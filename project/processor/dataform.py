import json
from datetime import datetime

contents_mornid = open('data/mornst_id.jl', "r").read() 
datas_mornid = [json.loads(str(item)) for item in contents_mornid.strip().split('\n')]

contents_rate = open('data/rate_sd.jl', "r").read() 
datas_rate = [json.loads(str(item)) for item in contents_rate.strip().split('\n')]

contents_his = open('data/historical.jl', "r").read() 
datas_his = [json.loads(str(item)) for item in contents_his.strip().split('\n')]

prices={isin["ISIN"]:[] for isin in datas_mornid}

#python date filtering
def filter(prices,datas_his,start,end):
    for data in datas_his:
        data["Date"]=datetime.strptime(data["Date"], "%A, %B %d, %Y")
        if data["Date"]<datetime.strptime(start,"%Y/%m/%d") or data["Date"]>datetime.strptime(end,"%Y/%m/%d"):
            continue
        prices[data["ISIN"]].append((data["Date"],data["Price"]))


filter(prices,datas_his,"2018/01/08","2021/01/08")
for isin in prices:
    sorted(prices[isin], key = lambda t: t[0])
    # sorted() function best case complexity is O(n)

modified_prices={isin["ISIN"]:[] for isin in datas_mornid}
#imputation
def impute(modified_prices,prices):
    for isin in prices:
        for pair in range(len(prices[isin])-1):
            diff=(prices[isin][pair][0]-prices[isin][pair+1][0]).days
            modified_prices[isin].append(float(prices[isin][pair][1]))
            if diff>1:
                price_now=float(prices[isin][pair][1])
                price_next=float(prices[isin][pair+1][1])
                ratio=(price_next/price_now)**(1/diff)
                next=price_now*ratio
                while diff>1:
                    #rounding only happens at output
                    modified_prices[isin].append(round(next,2))
                    next*=ratio
                    diff-=1
        modified_prices[isin].append(float(prices[isin][-1][1]))


impute(modified_prices,prices)

#find common start and end date
start=max(prices[isin][-1][0] for isin in prices)
end=min(prices[isin][0][0] for isin in prices)

for isin in prices:
    diff_end=(prices[isin][0][0]-end).days
    diff_start=(start-prices[isin][-1][0]).days
    modified_prices[isin]=modified_prices[isin][diff_end:len(modified_prices[isin])-diff_start]





# processing the data looks like [{'ISIN': '', '3_year_annalised': '', '3_year_sd': ''},{"prices":[]}]
process=[]
for data_m in datas_mornid:
    process.append({"ISIN":data_m["ISIN"]})

for data in process:
    for data_r in datas_rate:
        if data_r["ISIN"]==data["ISIN"]:
            if "3_year_annualised" in data_r:
                data["3_year_annalised"]=data_r["3_year_annualised"]
            else:
                data["3_year_sd"]=data_r["3_year_sd"]
    for isin in modified_prices:
        if data["ISIN"]==isin:
            data["prices"]=modified_prices[isin]
            break
output={"data":process,"meta":{"start":datetime.strftime(start,"%Y/%m/%d"),"end":datetime.strftime(end,"%Y/%m/%d")}}

with open('data_out/model_input.json', 'w') as outfile:
    json.dump(output, outfile)



    
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

contents_mornid=open('data/mornst_id.jl',"r").read() 
datas_mornid=[json.loads(str(item)) for item in contents_mornid.strip().split('\n')]

contents_rate=open('data/rate_sd.jl',"r").read() 
datas_rate=[json.loads(str(item)) for item in contents_rate.strip().split('\n')]

contents_his=open('data/historical.jl',"r").read() 
datas_his = [json.loads(str(item)) for item in contents_his.strip().split('\n')]


#python date filtering
prices={isin["ISIN"]:[] for isin in datas_mornid}

def filter(prices,datas_his,start,end):
    for data in datas_his:
        data["Date"]=datetime.strptime(data["Date"], "%A, %B %d, %Y")
        if data["Date"]<start or data["Date"]>end:
            continue
        prices[data["ISIN"]].append((data["Date"],data["Price"]))

# start_date=datetime.strptime("2018/01/08","%Y/%m/%d")
# end_date=datetime.strptime("2021/01/08","%Y/%m/%d")
start_date=datetime.today()-relativedelta(years=3)
end_date=datetime.today()
filter(prices,datas_his,start_date,end_date)
for isin in prices:
    sorted(prices[isin], key = lambda t: t[0])
    # sorted() function best case complexity is O(n)
    #prices are ordered according to descending order of dates from current date to history date for example(e.g.2021/01/08 - 2018/01/08 )


#imputation
modified_prices={isin["ISIN"]:[] for isin in datas_mornid}
def impute(modified_prices,prices):
    for isin in prices:
        for current in range(len(prices[isin])-1):
            diff=(prices[isin][current][0]-prices[isin][current+1][0]).days
            price_current=float(prices[isin][current][1].replace(",",""))
            modified_prices[isin].append(price_current)
            if diff>1:
                price_next=float(prices[isin][current+1][1].replace(",",""))
                ratio=(price_next/price_current)**(1/diff)
                next=price_current*ratio
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


#calculate return between days 
#gap can be changed to generate different rates arrays


def return_rate(modified_prices,rates,gap):
    for isin in modified_prices: 
        for step in range(0,len(modified_prices[isin])-gap,gap):
            rate=modified_prices[isin][step]/modified_prices[isin][step+gap]
            rates[isin].append(round(rate,4))



# input sampling frequency in days

# print("Choose a sampling frequency(besides 2,5,7,10,15,20,30,60)")
# # Do not always trust uer input, add constraints here !
# rate_input=int(input())



# name of sampling 
category=[2,5,7,15,30,60,90]
# category.append(rate_input)
rates={key:{isin["ISIN"]:[] for isin in datas_mornid} for key in category}
for rate in rates:
    return_rate(modified_prices,rates[rate],rate)



#data output looks like {data:[{'ISIN': '', '3_year_annalised': '', '3_year_sd': '',"prices":[]},...],meta:{'start':'','end:''}}
process=[]
for data_m in datas_mornid:
    process.append({"ISIN":data_m["ISIN"]})

for data in process:
    for data_r in datas_rate:
        if data_r["ISIN"]==data["ISIN"]:
            if "3_year_annualised" in data_r:
                data["3_year_annalised"]=float(data_r["3_year_annualised"])/100
            else:
                data["3_year_sd"]=round(float(data_r["3_year_sd"].strip('%'))/100,4)
    for rate in rates:
        data[f"window_{rate}"]=rates[rate][data["ISIN"]]
    
        
output={"data":process,"meta":{"end":datetime.strftime(end,"%Y/%m/%d"),"start":datetime.strftime(start,"%Y/%m/%d")}}


#output file
with open('data_out/model_input.json', 'w') as outfile:
    json.dump(output, outfile)



    
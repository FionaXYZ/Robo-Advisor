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







#processing the data looks like [{'ISIN': '', '3_year_annalised': '', '3_year_sd': ''},{....}]
# process=[]
# for data_m in datas_mornid:
#     process.append({"ISIN":data_m["ISIN"]})

# for data in process:
#     for data_r in datas_rate:
#         if data_r["ISIN"]==data["ISIN"]:
#             if "3_year_annualised" in data_r:
#                 data["3_year_annalised"]=data_r["3_year_annualised"]
#             else:
#                 data["3_year_sd"]=data_r["3_year_sd"]

# with open('../data_out/model_input.jl', 'w') as outfile:
#     for processed in process:
#         json.dump(processed, outfile)
#         outfile.write('\n')



    
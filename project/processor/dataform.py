import json

contents_mornid = open('../data/mornst_id.jl', "r").read() 
datas_mornid = [json.loads(str(item)) for item in contents_mornid.strip().split('\n')]

contents_rate = open('../data/rate_sd.jl', "r").read() 
datas_rate = [json.loads(str(item)) for item in contents_rate.strip().split('\n')]

contents_his = open('../data/mornst_id.jl', "r").read() 
datas_his = [json.loads(str(item)) for item in contents_mornid.strip().split('\n')]


#processing the data looks like [{'ISIN': '', '3_year_annalised': '', '3_year_sd': ''},{....}]
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

with open('../data_out/model_input.jl', 'w') as outfile:
    for processed in process:
        json.dump(processed, outfile)
        outfile.write('\n')



    
import json

contents_rate = open('../data/rate_sd.jl', "r").read() 
datas_rate = [json.loads(str(item)) for item in contents_rate.strip().split('\n')]

contents_mornid = open('../data/mornst_id.jl', "r").read() 
datas_mornid = [json.loads(str(item)) for item in contents_mornid.strip().split('\n')]

#change mornst_id to ISIN 
for data_r in datas_rate:
    for data_m in datas_mornid:
        if data_m["mornst_id"]==data_r["mornst_id"]:
            del data_r["mornst_id"]
            data_r["ISIN"]=data_m["ISIN"]
            break

#new form of data looks like [{'ISIN': '', '3_year_annalised': '', '3_year_sd': ''},{....}]
new_form=[]
for data_m in datas_mornid:
    new_form.append({"ISIN":data_m["ISIN"]})

for data in new_form:
    for data_r in datas_rate:
        if data_r["ISIN"]==data["ISIN"]:
            if "3_year_annualised" in data_r:
                data["3_year_annalised"]=data_r["3_year_annualised"]
            else:
                data["3_year_sd"]=data_r["3_year_sd"]

with open('../data_out/rate_sd.jl', 'w') as outfile:
    for processed in new_form:
        json.dump(processed, outfile)
        outfile.write('\n')

    
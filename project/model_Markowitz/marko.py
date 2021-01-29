import numpy as np
import json
import math

with open('data_out/model_input.json') as json_file:
    data = json.load(json_file)


# covariance matrix
all=[]
std=[]
returns=[]

for datas in data["data"]:
    all.append(datas["rates"])
    std.append(datas["3_year_sd"])
    returns.append(datas["3_year_annalised"])

print(returns)
rates=np.array(all)
covMatrix = np.cov(rates,bias=True)

mod=std/(np.diag(covMatrix)**0.5)

model_input=mod*covMatrix*np.array(mod)[np.newaxis].T
#np.diag(mod)*covMatrix*np.diag(mod) == np.diag(np.array(std)**2)


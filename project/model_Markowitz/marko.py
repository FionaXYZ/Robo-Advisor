import numpy as np
import json
import cvxpy as cp
import matplotlib.pyplot as plt
import os
import mpld3
from mpld3 import plugins

os.system("scrapy crawl mornst_id --nolog")
os.system("scrapy crawl rate_sd --nolog")
os.system("scrapy crawl unit --nolog")
os.system("scrapy crawl ftid_no --nolog")
os.system("scrapy crawl historical --nolog")
os.system("python3 processor/dataform.py")

with open('data_out/model_input.json') as json_file:
    data = json.load(json_file)

# user-input
with open('backend/user_input.json') as json_file:
   input=json.load(json_file)
input=input["isins"]
for isin in input:
    if isin["isin"]!="risk-free":
        continue
    rf=float(isin["rate"])/100


category=[]
for name in data['data'][0]:
    category.append(name)
category=category[3:]

# name of all the assets
title=[]
for stock in data['data']:
    title.append(stock["ISIN"])
title.append("risk-free")

rates={key:[] for key in category}
res={key:{"weights":[],"variance":[]} for key in category}

std=[]
returns=[]
for datas in data["data"]:
    std.append(datas["3_year_sd"])
    returns.append(datas["3_year_annalised"])

# adding risk free asset to the model
# rf=0.0045
returns.append(rf)
n_assets=len(returns)
returns=np.array(returns)
maxi=np.max(returns)
# print(f"maximum possible return you can choose is {maxi}")
zeros=np.array([np.zeros((n_assets-1,), dtype=int)])
zeros_vertical=np.array([np.zeros((n_assets,),dtype=int)])


mini=rf
# print(f"The possible minimum return available {mini}")
# find the returns on efficient frontier
target_returns=[]
while mini<maxi:
    target_returns.append(round(mini,4))
    mini+=0.0025
target_returns.append(maxi)


# add user input constraints
def add_constraints(input,constraints,title):
    for isin in input:
        index=title.index(isin["isin"])
        if isin["constraint"]!="None" and isin["constraint_op1"]!=None:
            if isin["constraint"]=="\u2265":
                constraints.extend([w[index]>=isin["constraint_op1"]])
            else:
                constraints.extend([w[index]<=isin["constraint_op1"]])


# Get and Draw efficient frontier for different sampling rate
for rate in rates:
    for datas in data["data"]:
        rates[rate].append(datas[rate])
    rates[rate]=np.array(rates[rate])
    covMatrix=np.cov(rates[rate])
    mod=std/(np.diag(covMatrix)**0.5)
    model_input=np.matmul(np.matmul(np.diag(mod),covMatrix),np.diag(mod))
    model_input=np.append(model_input, zeros, axis=0)
    model_input=np.append(model_input, zeros_vertical.transpose(), axis=1)
    for target in target_returns:
        w=cp.Variable(n_assets)
        constraints=[w.T@returns>=target,cp.sum(w)==1,w>=0]
        add_constraints(input,constraints,title)
        marko=cp.Problem(cp.Minimize((1/2)*cp.quad_form(w, model_input)),constraints)
        marko.solve()
        if w.value is None:
            end=target_returns.index(target)
            target_returns=target_returns[:end]
            break
            # res[rate]["weights"].append([np.NAN]*n_assets)
        else:
            maxi=target
            res[rate]["weights"].append(w.value)
        if target==target_returns[0]:
            mini=np.around(np.dot(w.value,returns),decimals=4)
        res[rate]["variance"].append(marko.value)

max_mini={"range_max":maxi,"range_min":mini}
with open('output/range.json','w') as outfile:
    json.dump(max_mini, outfile)



# plot return vs risk
fig=plt.figure(1,figsize=(9,7))
for rate in res:
    WCW=res[rate]["variance"]
    plt.plot(WCW, target_returns,'o',label=f'{rate}')

plt.xlabel('WCW')
plt.ylabel('returns')
plt.legend()
# mpld3.save_html(fig,"output/frontier.html")
mpld3.fig_to_dict(fig)
mpld3.save_json(fig,'output/frontier.json')


# get average weights of the assets and boundary
weights={key:{"weights":[]} for key in target_returns}
number=0
for ret in target_returns:
    for rate in res: 
        weights[ret]["weights"].append(res[rate]["weights"][number])
    number=number+1

weights_avg={key:{"mean":[],"max":[],"min":[]} for key in target_returns}  


for ret in target_returns:
    mean=np.mean(weights[ret]["weights"],axis=0)
    weights_avg[ret]["mean"].append(np.around(mean,decimals=4))
    max=np.amax(weights[ret]["weights"],axis=0)
    min=np.amin(weights[ret]["weights"],axis=0)
    weights_avg[ret]["max"].append(np.around(max,decimals=4))
    weights_avg[ret]["min"].append(np.around(min,decimals=4))


# new format
asset=0
allocation=[]
max_array=[]
min_array=[]
while asset<n_assets:
    weight=[]
    ma=[]
    mi=[]
    for ret in target_returns: 
        weight.append(weights_avg[ret]["mean"][0][asset])
        ma.append(weights_avg[ret]["max"][0][asset])
        mi.append(weights_avg[ret]["min"][0][asset])
    asset=asset+1
    allocation.append(weight)
    max_array.append(ma)
    min_array.append(mi)

fig2=plt.figure(2,figsize=(9,7))
for asset in range(len(allocation)):
    plt.plot(target_returns,allocation[asset],label=f'{title[asset]}')
    plt.fill_between(target_returns,max_array[asset],min_array[asset],alpha=0.5)
plt.xlabel('returns')
plt.ylabel('weights')
plt.legend()
# mpld3.save_html(fig2,"output/allocation.html")
mpld3.fig_to_dict(fig2)
mpld3.save_json(fig2,'output/allocation.json')


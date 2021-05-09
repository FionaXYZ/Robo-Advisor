import numpy as np
import json
import math
import cvxpy as cp
import matplotlib.pyplot as plt

with open('data_out/model_input.json') as json_file:
    data = json.load(json_file)


category=[]
for name in data['data'][0]:
    category.append(name)
category=category[3:]

rates={key:[] for key in category}
res={key:{"weights":[],"variance":[]} for key in category}

std=[]
returns=[]
for datas in data["data"]:
    std.append(datas["3_year_sd"])
    returns.append(datas["3_year_annalised"])

n_assets=len(returns)
returns = np.array(returns)
print(f"maximum return you can choose is {max(returns)}")
# minimum=min(returns)
# print(minimum)
target_returns=[10,10.25,10.5,10.75,11,11.25,11.5,11.75,12,12.25,12.5,12.75,13,13.25,13.5,13.75,14]

for rate in rates:
    for datas in data["data"]:
        rates[rate].append(datas[rate])
    rates[rate]=np.array(rates[rate])
    covMatrix=np.cov(rates[rate],bias=True)
    mod=std/(np.diag(covMatrix)**0.5)
    model_input=mod*covMatrix*np.array(mod)[np.newaxis].T
    for target in target_returns:
        w = cp.Variable(n_assets)
        marko = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w, model_input)), [w.T * returns >= target, cp.sum(w) == 1, w>=0])
        marko.solve()
        res[rate]["weights"].append(w.value)
        res[rate]["variance"].append(marko.value)

# curve={}
# begin=res[category[0]]["variance"]
# for rate in res:
#     if res[rate]["variance"]>begin:
#         curve[rate]=res[rate]
# print(curve)


for rate in res:
    WCW=res[rate]["variance"]
    plt.plot(WCW, target_returns,'o',label=f'{rate}')


plt.xlabel('WCW')
plt.ylabel('returns')
plt.legend()
plt.show()

weights={key:{"weights":[]} for key in target_returns}
number=0
for returns in target_returns:
    for rate in res: 
        weights[returns]["weights"].append(res[rate]["weights"][number])
    number=number+1

weights_avg={key:{"mean":[],"difference":[]} for key in target_returns}  

for returns in target_returns:
    diff=[]
    mean=np.mean(weights[returns]["weights"],axis=0)
    weights_avg[returns]["mean"].append(mean)
    max=np.amax(weights[returns]["weights"],axis=0)
    min=np.amin(weights[returns]["weights"],axis=0)
    diff.append(max-mean)
    diff.append(mean-min)
    weights_avg[returns]["difference"].append(np.amax(diff,axis=0))


asset=0
allocation=[]
while asset<n_assets:
    weight=[]
    for returns in target_returns: 
        weight.append(weights_avg[returns]["mean"][0][asset])
    asset=asset+1
    allocation.append(weight)

number=0
for asset in allocation:
    plt.plot(target_returns,asset,label=f'w{number}')
    number=number+1


plt.xlabel('returns')
plt.ylabel('weights')
plt.legend()
plt.show()


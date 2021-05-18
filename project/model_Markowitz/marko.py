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

# adding risk free asset to the model
rf=0.0045
returns.append(rf)
n_assets=len(returns)
returns=np.array(returns)
maxi=max(returns)
print(f"maximum return you can choose is {maxi}")
zeros=np.array([np.zeros((n_assets-1,), dtype=int)])
zeros_vertical=np.array([np.zeros((n_assets,),dtype=int)])


mini=rf
print(f"The minimum return available {mini}")
# find the returns on efficient frontier
target_returns=[]
while mini<maxi:
    target_returns.append(mini)
    mini+=0.0025
target_returns.append(maxi)


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
        marko=cp.Problem(cp.Minimize((1/2)*cp.quad_form(w, model_input)),[w.T*returns>=target,cp.sum(w) == 1,w>=0])
        marko.solve()
        res[rate]["weights"].append(w.value)
        res[rate]["variance"].append(marko.value)

for rate in res:
    WCW=res[rate]["variance"]
    plt.plot(WCW, target_returns,'o',label=f'{rate}')


plt.xlabel('WCW')
plt.ylabel('returns')
plt.legend()
plt.show()

weights={key:{"weights":[]} for key in target_returns}
number=0
for ret in target_returns:
    for rate in res: 
        weights[ret]["weights"].append(res[rate]["weights"][number])
    number=number+1

weights_avg={key:{"mean":[],"difference":[]} for key in target_returns}  

for ret in target_returns:
    diff=[]
    mean=np.mean(weights[ret]["weights"],axis=0)
    weights_avg[ret]["mean"].append(mean)
    max=np.amax(weights[ret]["weights"],axis=0)
    min=np.amin(weights[ret]["weights"],axis=0)
    diff.append(max-mean)
    diff.append(mean-min)
    weights_avg[ret]["difference"].append(np.amax(diff,axis=0))

print(weights_avg)

asset=0
allocation=[]
while asset<n_assets:
    weight=[]
    for ret in target_returns: 
        weight.append(weights_avg[ret]["mean"][0][asset])
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


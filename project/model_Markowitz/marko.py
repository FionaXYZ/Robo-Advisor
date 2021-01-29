import numpy as np
import json
import math
from scipy.optimize import minimize

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


rates=np.array(all)
covMatrix = np.cov(rates,bias=True)

mod=std/(np.diag(covMatrix)**0.5)

model_input=mod*covMatrix*np.array(mod)[np.newaxis].T
#np.diag(mod)*covMatrix*np.diag(mod) == np.diag(np.array(std)**2)


n_assets=len(returns)
returns = np.array(returns)


def make_marko(C):
    def marko(w):
        return w.dot(C.dot(w))
    return  marko

def make_eq(target,R):
    return lambda w: target-w.dot(R)

def summ(w):
    return 1.0 - np.sum(w)

init=np.random.rand(n_assets)
w0 = init/sum(init)
# w0 = [1/n_assets]*n_assets
# w0=np.array(w0)

bounds = ((0.0, 1.0),) * len(returns)

def optimal(target):
    weights = minimize(make_marko(model_input), w0, method='SLSQP', constraints=({'type': 'eq', 'fun': make_eq(target,returns)},{'type': 'eq', 'fun': summ}),bounds=bounds)
    return weights

def frontier(targets):
    frontier = []
    for t in targets:
        frontier.append(optimal(t))
    return frontier

target_returns=[2,4,6,7,8,9,10,10.5,11,11.5,12,12.5,13,13.5,14]
effcient_frontier=frontier(target_returns)
print(effcient_frontier)
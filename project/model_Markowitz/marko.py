import numpy as np
import json
import math
# from scipy.optimize import minimize
import cvxpy as cp

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

# using scipy.optimize library
# def make_marko(C):
#     def marko(w):
#         return w.dot(C.dot(w))
#     return  marko
# def make_eq(target,R):
#     return lambda w: target-w.dot(R)
# def summ(w):
#     return 1.0 - np.sum(w)
# init=np.random.rand(n_assets)
# w0 = init/sum(init)
# bounds = ((0.0, 1.0),) * len(returns)
# def optimal(target):
#     weights = minimize(make_marko(model_input), w0, method='SLSQP', constraints=({'type': 'eq', 'fun': make_eq(target,returns)},{'type': 'eq', 'fun': summ}),bounds=bounds)
#     return weights


# using cvxpy library
target_returns=[2,4,6,7,8,9,10,10.5,11,11.5,12,12.5,13,13.5,14]
res=[]

# using cvxpy library
for target in target_returns:
    w = cp.Variable(n_assets)
    prob = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w, model_input)), [w.T * returns >= target, cp.sum(w) == 1, w>=0])
    prob.solve()

    res.append(prob.value)
    print(w.value)
print(res)
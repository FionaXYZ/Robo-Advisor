import numpy as np
import json
import math
# from scipy.optimize import minimize
import cvxpy as cp

with open('data_out/model_input.json') as json_file:
    data = json.load(json_file)


# covariance matrix
ratio_1=[]
ratio_2=[]
ratio_5=[]
ratio_7=[]
ratio_10=[]
ratio_15=[]
ratio_20=[]
ratio_30=[]
std=[]
returns=[]

for datas in data["data"]:
    ratio_1.append(datas["rates_1"])
    ratio_2.append(datas["rates_2"])
    ratio_5.append(datas["rates_5"])
    ratio_7.append(datas["rates_7"])
    ratio_10.append(datas["rates_10"])
    ratio_15.append(datas["rates_15"])
    ratio_20.append(datas["rates_20"])
    ratio_30.append(datas["rates_30"])
    std.append(datas["3_year_sd"])
    returns.append(datas["3_year_annalised"])


rates_1=np.array(ratio_1)
rates_2=np.array(ratio_2)
rates_5=np.array(ratio_5)
rates_7=np.array(ratio_7)
rates_10=np.array(ratio_10)
rates_15=np.array(ratio_15)
rates_20=np.array(ratio_20)
rates_30=np.array(ratio_30)

covMatrix_1 = np.cov(rates_1,bias=True)
covMatrix_2 = np.cov(rates_2,bias=True)
covMatrix_5 = np.cov(rates_5,bias=True)
covMatrix_7 = np.cov(rates_7,bias=True)
covMatrix_10 = np.cov(rates_10,bias=True)
covMatrix_15 = np.cov(rates_15,bias=True)
covMatrix_20 = np.cov(rates_20,bias=True)
covMatrix_30 = np.cov(rates_30,bias=True)

mod_1=std/(np.diag(covMatrix_1)**0.5)
mod_2=std/(np.diag(covMatrix_2)**0.5)
mod_5=std/(np.diag(covMatrix_5)**0.5)
mod_7=std/(np.diag(covMatrix_7)**0.5)
mod_10=std/(np.diag(covMatrix_10)**0.5)
mod_15=std/(np.diag(covMatrix_15)**0.5)
mod_20=std/(np.diag(covMatrix_20)**0.5)
mod_30=std/(np.diag(covMatrix_30)**0.5)


model_input_1=mod_1*covMatrix_1*np.array(mod_1)[np.newaxis].T
model_input_2=mod_2*covMatrix_2*np.array(mod_2)[np.newaxis].T
model_input_5=mod_5*covMatrix_5*np.array(mod_5)[np.newaxis].T
model_input_7=mod_7*covMatrix_7*np.array(mod_7)[np.newaxis].T
model_input_10=mod_10*covMatrix_10*np.array(mod_10)[np.newaxis].T
model_input_15=mod_15*covMatrix_15*np.array(mod_15)[np.newaxis].T
model_input_20=mod_20*covMatrix_20*np.array(mod_20)[np.newaxis].T
model_input_30=mod_30*covMatrix_30*np.array(mod_30)[np.newaxis].T

#np.diag(mod)*covMatrix*np.diag(mod) == np.diag(np.array(std)**2)


n_assets=len(returns)
returns = np.array(returns)


# using cvxpy library
print(f"maximum return you can choose is {max(returns)}")
target_returns=[10,10.5,11,11.5,12,12.5,13,13.5,14]
res=[]

# using cvxpy library
for target in target_returns:
    w_1 = cp.Variable(n_assets)
    w_2 = cp.Variable(n_assets)
    w_5 = cp.Variable(n_assets)
    w_7 = cp.Variable(n_assets)
    w_10 = cp.Variable(n_assets)
    w_15 = cp.Variable(n_assets)
    w_20 = cp.Variable(n_assets)
    w_30 = cp.Variable(n_assets)




    marko_1 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_1, model_input_1)), [w_1.T * returns >= target, cp.sum(w_1) == 1, w_1>=0])
    marko_1.solve()
    marko_2 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_2, model_input_2)), [w_2.T * returns >= target, cp.sum(w_2) == 1, w_2>=0])
    marko_2.solve()
    marko_5 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_5, model_input_5)), [w_5.T * returns >= target, cp.sum(w_5) == 1, w_5>=0])
    marko_5.solve()
    marko_7 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_7, model_input_7)), [w_7.T * returns >= target, cp.sum(w_7) == 1, w_7>=0])
    marko_7.solve()
    marko_10 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_10, model_input_10)), [w_10.T * returns >= target, cp.sum(w_10) == 1, w_10>=0])
    marko_10.solve()
    marko_15 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_15, model_input_15)), [w_15.T * returns >= target, cp.sum(w_15) == 1, w_15>=0])
    marko_15.solve()
    marko_20 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_20, model_input_20)), [w_20.T * returns >= target, cp.sum(w_20) == 1, w_20>=0])
    marko_20.solve()
    marko_30 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_30, model_input_30)), [w_30.T * returns >= target, cp.sum(w_30) == 1, w_30>=0])
    marko_30.solve()

    print(target)
    print(f"weights with gap1 {w_1.value}")
    print(marko_1.value)
    print(f"weights with gap2 {w_2.value}")
    print(marko_2.value)
    print(f"weights with gap5 {w_5.value}")
    print(marko_5.value)
    print(f"weights with gap7 {w_7.value}")
    print(marko_7.value)
    print(f"weights with gap10 {w_10.value}")
    print(marko_10.value)
    print(f"weights with gap15 {w_15.value}")
    print(marko_15.value)
    print(f"weights with gap20 {w_20.value}")
    print(marko_20.value)
    print(f"weights with gap30 {w_30.value}")
    print(marko_30.value)








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
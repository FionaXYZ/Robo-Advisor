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



for rate in res:
    WCW=res[rate]["variance"]
    plt.plot(WCW, target_returns,'o',label=f'{rate}')


plt.xlabel('WCW')
plt.ylabel('returns')
plt.legend()
plt.show()


# for datas in data["data"]:
#     ratio_1.append(datas["rates_1"])
#     ratio_2.append(datas["rates_2"])
#     ratio_5.append(datas["rates_5"])
#     ratio_7.append(datas["rates_7"])
#     ratio_15.append(datas["rates_15"])
#     ratio_30.append(datas["rates_30"])
#     ratio_in.append(data["input_sampling"])
#     std.append(datas["3_year_sd"])
#     returns.append(datas["3_year_annalised"])






# rates_1=np.array(ratio_1)
# rates_2=np.array(ratio_2)
# rates_5=np.array(ratio_5)
# rates_7=np.array(ratio_7)
# rates_15=np.array(ratio_15)
# rates_30=np.array(ratio_30)
# rates_in=np.array(ratio_in)

# covMatrix_1 = np.cov(rates_1,bias=True)
# covMatrix_2 = np.cov(rates_2,bias=True)
# covMatrix_5 = np.cov(rates_5,bias=True)
# covMatrix_7 = np.cov(rates_7,bias=True)
# covMatrix_15 = np.cov(rates_15,bias=True)
# covMatrix_30 = np.cov(rates_30,bias=True)
# covMatrix_in=np.cov(rates_in,bias=True)

# mod_1=std/(np.diag(covMatrix_1)**0.5)
# mod_2=std/(np.diag(covMatrix_2)**0.5)
# mod_5=std/(np.diag(covMatrix_5)**0.5)
# mod_7=std/(np.diag(covMatrix_7)**0.5)
# mod_15=std/(np.diag(covMatrix_15)**0.5)
# mod_30=std/(np.diag(covMatrix_30)**0.5)
# mod_in=std/(np.diag(covMatrix_in)**0.5)

# model_input_1=mod_1*covMatrix_1*np.array(mod_1)[np.newaxis].T
# model_input_2=mod_2*covMatrix_2*np.array(mod_2)[np.newaxis].T
# model_input_5=mod_5*covMatrix_5*np.array(mod_5)[np.newaxis].T
# model_input_7=mod_7*covMatrix_7*np.array(mod_7)[np.newaxis].T
# model_input_15=mod_15*covMatrix_15*np.array(mod_15)[np.newaxis].T
# model_input_30=mod_30*covMatrix_30*np.array(mod_30)[np.newaxis].T
# model_input_in=mod_in*covMatrix_in*np.array(mod_in)[np.newaxis].T

# #np.diag(mod)*covMatrix*np.diag(mod) == np.diag(np.array(std)**2)


# n_assets=len(returns)
# returns = np.array(returns)


# # using cvxpy library
# print(f"maximum return you can choose is {max(returns)}")
# target_returns=[10,10.5,11,11.5,12,12.5,13,13.5,14]
# res=[]

# using cvxpy library
# for target in target_returns:
#     w_1 = cp.Variable(n_assets)
#     w_2 = cp.Variable(n_assets)
#     w_5 = cp.Variable(n_assets)
#     w_7 = cp.Variable(n_assets)
#     w_15 = cp.Variable(n_assets)
#     w_30 = cp.Variable(n_assets)
#     w_in = cp.Variable(n_assets)




#     marko_1 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_1, model_input_1)), [w_1.T * returns >= target, cp.sum(w_1) == 1, w_1>=0])
#     marko_1.solve()
#     marko_2 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_2, model_input_2)), [w_2.T * returns >= target, cp.sum(w_2) == 1, w_2>=0])
#     marko_2.solve()
#     marko_5 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_5, model_input_5)), [w_5.T * returns >= target, cp.sum(w_5) == 1, w_5>=0])
#     marko_5.solve()
#     marko_7 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_7, model_input_7)), [w_7.T * returns >= target, cp.sum(w_7) == 1, w_7>=0])
#     marko_7.solve()
#     marko_10 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_10, model_input_10)), [w_10.T * returns >= target, cp.sum(w_10) == 1, w_10>=0])
#     marko_10.solve()
#     marko_15 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_15, model_input_15)), [w_15.T * returns >= target, cp.sum(w_15) == 1, w_15>=0])
#     marko_15.solve()
#     marko_20 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_20, model_input_20)), [w_20.T * returns >= target, cp.sum(w_20) == 1, w_20>=0])
#     marko_20.solve()
#     marko_30 = cp.Problem(cp.Minimize((1/2)*cp.quad_form(w_30, model_input_30)), [w_30.T * returns >= target, cp.sum(w_30) == 1, w_30>=0])
#     marko_30.solve()

#     print(target)
#     print(f"weights with gap1 {w_1.value}")
#     print(marko_1.value)
#     print(f"weights with gap2 {w_2.value}")
#     print(marko_2.value)
#     print(f"weights with gap5 {w_5.value}")
#     print(marko_5.value)
#     print(f"weights with gap7 {w_7.value}")
#     print(marko_7.value)
#     print(f"weights with gap10 {w_10.value}")
#     print(marko_10.value)
#     print(f"weights with gap15 {w_15.value}")
#     print(marko_15.value)
#     print(f"weights with gap20 {w_20.value}")
#     print(marko_20.value)
#     print(f"weights with gap30 {w_30.value}")
#     print(marko_30.value)







# # target_returns=[2,4,6,7,8,9,10,10.5,11,11.5,12,12.5,13,13.5,14]
# # WCW = [0.025740079575258142, 0.01837975269826956, 0.013842462024228409, 0.012602604105005952, 0.011757255802028788, 0.011187926708233488, 0.0108257447721793, 0.010757046740613365, 0.010848824190930854, 0.011103696362026167, 0.011610016793812069, 0.012446757332571976, 0.013576799468538354, 0.015065081240326716, 0.01686352475001811]
# target_returns=[2,4,6,7,8,9,10,10.5,11,11.5,12,12.5,13,13.5,14,15,16,17,19,20]
# WCW = [0.010290609169348207, 0.008319508194950722, 0.006848749266459986, 0.006300998069429644, 0.005878332383875992, 0.005580752209799022, 0.00540825754719874, 0.005368917282702355, 0.005360848396075144, 0.005384050887317103, 0.005438524756428235, 0.005524270003408539, 0.0056412866282580095, 0.005789574630976654, 0.005969134011564474, 0.006422066906347622, 0.007000085312607454, 0.007703189230343975, 0.00948465360024707, 0.010563014052413652]

# plt.plot(WCW, target_returns)
# plt.xlabel('WCW')
# plt.ylabel('returns')

# plt.show()


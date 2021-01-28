import numpy as np
import json

with open('data_out/model_input.json') as json_file:
    data = json.load(json_file)


# covariance matrix
all=[]
for price in data["data"]:
    all.append(price["rates"])
rates=np.array(all)
covMatrix = np.cov(rates,bias=True)

print(covMatrix)
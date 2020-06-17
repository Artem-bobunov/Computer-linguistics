import pandas as pd
import numpy as np
import os
import json
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

CountScore = 4

def tokenize(row):
    text = [row]
    res = model.predict(text, k=CountScore)
    #print(res)
    return res


tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)




if __name__ == "__main__":

    file_one = pd.read_json('C:/Users/wlcom/Downloads/positiv.json')
    lists = file_one['Column1'].tolist()
    newLemms = list()
    path = "D:/result" + str(1) + ".json"



    if not os.path.exists(path):
        for index, elem in enumerate(lists):
            t = tokenize(elem)[0]
            newLemms.append(t)
            print(index, " - ", t)

        with open(path, "tw", encoding='utf-8') as f:
            json.dump(newLemms, f, indent=4)
    else:
        with open(path, "tr", encoding='utf-8') as f:
            newLemms = json.load(f)

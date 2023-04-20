import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.model_selection import cross_validate
from sklearn import tree,neighbors,svm, ensemble
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pickle
import matplotlib.pyplot as plt

def pro(data):
    tool = OneHotEncoder()
    key = ['Gender','Polyuria','Polydipsia','sudden weight loss', 'weakness', 'Polyphagia' ,'Genital thrush','visual blurring','Itching','Irritability','delayed healing','partial paresis','muscle stiffness','Alopecia','Obesity']

    x1 = tool.fit_transform(data[key]).toarray()    #onehot인코더를 사용하면 값을 배열로 바꿔주는 과정이 필요함!
    pickle.dump(tool, open("tool.t","wb"))
    return x1
    

def data():
    data = pd.read_csv("./app001/dataset/data.csv")

    x1 = pro(data)
    x = data.iloc[:,[0]].values
    x = np.hstack([x,x1])
    y = data.iloc[:,16].values

    
    train_input, test_input, train_target, test_target = train_test_split(x,y,test_size=0.2)
    return train_input, test_input, train_target, test_target

def make_model():
    model = ensemble.RandomForestClassifier(n_jobs=-1)
    return model

def do_learn():
    train_input, test_input, train_target, test_target = data()
    model = make_model()
    scores = cross_validate(model, train_input, train_target, return_train_score=True, n_jobs=-1)

    model.fit(train_input, train_target)
    train_score = model.score(train_input, train_target)
    score = model.score(test_input, test_target)
    #성능 평균 및 최저점 분석
    trainlist = list()
    testlist= list()
    crosstrain = list()
    crosstest = list()
    turnvalue= 1000
    for i in range(turnvalue):
        train_input, test_input, train_target, test_target = data()
        model.fit(train_input,train_target)
        scores = cross_validate(model, train_input, train_target, return_train_score=True, n_jobs=-1)
        trainlist.append(model.score(train_input,train_target))
        testlist.append(model.score(test_input,test_target))
        crosstrain.append(np.mean(scores['train_score']))
        crosstest.append(np.mean(scores['test_score']))
        print(f"{i}번째 완료!")
    print("score min:", "train:",np.min(trainlist) ,"test:", np.min(testlist))
    print("score mean:", "train:",np.mean(trainlist) ,"test:", np.mean(testlist))
    print("cross score min:", "train:",np.min(crosstrain) ,"test:", np.min(crosstest))
    print("cross score mean:", "train:",np.mean(crosstrain) ,"test:", np.mean(crosstest))

    pickle.dump(model, open("model2.t","wb"))
    
    
do_learn()

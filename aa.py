#!/usr/bin/python  
# -*- coding: gbk -*-  

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

train = pd.read_csv("D:/train.csv", dtype={"Age": np.float64},)


def harmonize_data(titanic):
    # 填充空数据 和 把string数据转成integer表示

    titanic["Age"] = titanic["Age"].fillna(titanic["Age"].median())

    titanic.loc[titanic["Sex"] == "male", "Sex"] = 0
    titanic.loc[titanic["Sex"] == "female", "Sex"] = 1

    titanic["Embarked"] = titanic["Embarked"].fillna("S")

    titanic.loc[titanic["Embarked"] == "S", "Embarked"] = 0
    titanic.loc[titanic["Embarked"] == "C", "Embarked"] = 1
    titanic.loc[titanic["Embarked"] == "Q", "Embarked"] = 2

    titanic["Fare"] = titanic["Fare"].fillna(titanic["Fare"].median())

    return titanic

train_data = harmonize_data(train)

predictors = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]
results = []
# 最小叶子数
sample_leaf_options = list(range(10, 30, 2))
# 树的数量
n_estimators_options = list(range(100, 500, 50))
# 最大深度
max_depth_options = list(range(1, 10, 1))
start = 0 
groud_truth = train_data['Survived'][start:]

results_data = train_data[start:]

train_data_sample = train_data.sample(frac=0.7)
print 'Survived=1'
print train_data_sample[train_data_sample['Survived']==1].shape[0]
print 'Survived=0'
print train_data_sample[train_data_sample['Survived']==0].shape[0]
#for leaf_size in sample_leaf_options:
#    for n_estimators_size in n_estimators_options:
#		for max_depth_size in max_depth_options:
leaf_size = 10
n_estimators_size = 500
max_depth_size = 8
alg = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
	max_depth=max_depth_size, max_features='auto', max_leaf_nodes=None,
	min_impurity_decrease=0.0, min_impurity_split=None,
	min_samples_leaf=leaf_size, min_samples_split=8,
	min_weight_fraction_leaf=0.0, n_estimators=n_estimators_size, n_jobs=1,
	oob_score=False, random_state=50, verbose=0, warm_start=False)
	
alg.fit(train_data_sample[predictors], train_data_sample['Survived'])
predict = alg.predict(train_data[predictors][start:])
# 用一个三元组，分别记录当前的 min_samples_leaf，n_estimators， 和在测试数据集上的精度
results.append((leaf_size, n_estimators_size, (groud_truth == predict).mean()))
# 真实结果和预测结果进行比较，计算准确率
print((groud_truth == predict).mean())

results_data.insert(12,'Predict',predict)
results_data.to_csv('D:/results.csv')
# 打印精度最大的那一个三元组
print(max(results, key=lambda x: x[2]))
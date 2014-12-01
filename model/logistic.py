#! /usr/bin/python
# coding: utf-8

import sys
import pandas as pd
from sklearn import linear_model

def main():
    train = pd.read_csv('train.csv')
    logistic = linear_model.LogisticRegression()
    y = train['Burst']
    X = train[['Hashtag','Mention','URL','Length','Reply','Follower','Follow','Favorite','Entry']]
    logistic.fit(X, y)
    print logistic.coef_ # 回帰係数（オッズ比）
    print logistic.intercept_ # 切片
    print logistic.score(X, y) # 決定係数

if __name__ == '__main__':
    main()

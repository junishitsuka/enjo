#! /usr/bin/python
# coding: utf-8

from sklearn.cluster import KMeans
import MySQLdb, sys
import numpy as np

def rtcount():
    sql = 'select retweet_count from enjo_basedata where retweet_id = "0" and retweet_count != "0" order by retweet_count asc'
    cursor.execute(sql)
    result = cursor.fetchall()
    return [[r[0]] for r in result]

def main():
    X = rtcount()
    k_means= KMeans(init='random', n_clusters=3)
    k_means.fit(X)
    Y=k_means.labels_

    f = open('output.txt', 'w')
    for i,y in enumerate(Y):
        f.write(str(X[i][0]) + ',' + str(y) + '\n')
    f.close()

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()
    main()

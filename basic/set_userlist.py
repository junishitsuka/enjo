#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys, math

DATA_SET = ['cover', 'namapo', 'kenketsu', 'spirits']

def get_userlists():
    userlists = set([])
    for i in range(len(DATA_SET)):
        data = open('../data/%s/community_userid.csv' % DATA_SET[i], 'r').readlines()
        for j in range(len(data)):
            if j == 0: continue # skip the header line
            d = data[j].split(',')
            for k in range(len(d)):
                if k > 1: userlists.add(d[k]) # skip meaningless elements
    return userlists

def main():
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()

    userlists = get_userlists()
    for user in list(userlists):
        sql = 'INSERT INTO enjo_users (name) VALUE ("%s")' % user
        cursor.execute(sql)
        connector.commit()

    cursor.close()
    connector.close()

main()

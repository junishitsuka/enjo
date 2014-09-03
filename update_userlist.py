#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys, math

DATA_SET = ['cover', 'namapo', 'kenketsu', 'spirits']

def main():
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()

    userlists = [[], [], [], []]
    for i in range(len(DATA_SET)):
        data = open('../data/%s/community_userid.csv' % DATA_SET[i], 'r').readlines()
        for j in range(len(data)):
            if j == 0: continue # skip the header line
            d = data[j].split(',')
            for k in range(len(d)):
                if k > 1:
                    sql = 'UPDATE enjo_users SET %s_communityid = %d WHERE name = "%s"' % (DATA_SET[i], int(d[0]), d[k])
                    cursor.execute(sql)
                    connector.commit()


    cursor.close()
    connector.close()

main()

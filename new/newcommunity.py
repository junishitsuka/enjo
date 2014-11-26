#! /usr/bin/python
# coding: utf-8

import sys, MySQLdb

FILE = '../../../enjo/data/output/subsubsubcluster_sorted.csv'

def main():
    f = open(FILE, 'r')
    line = f.readline()
    while line:
        target = line.rstrip().split(',')
        if int(target[1]) < 100: break

        sql = 'insert into enjo_communities (community_id, member) values ("%s", %d)' % (target[0], int(target[1]))
        print sql
        cursor.execute(sql)
        connector.commit()

        line = f.readline()


if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()
    main()

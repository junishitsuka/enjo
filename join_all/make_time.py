#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys

DATA_SET = ['namapo', 'kenketsu', 'spirits']

def main():
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()

    for topic in DATA_SET:
        f = open('../../data/%s/basedata.dat' % topic, 'r')
        line = f.readline()
        while line:
            base = line.split('\t')
            t = base[1].split(' ')
            date = t[0].split('/')
            time = t[1].split(':')
            d = date[0] + '-' + date[1] + '-' + date[2] + ' ' + time[0] + ':' + time[1] + ':' + time[2]
            sql = 'INSERT INTO enjo_time (topic, time, username) VALUE ("%s", "%s", "%s")' % (topic, d, base[6])
            cursor.execute(sql)
            connector.commit()

            line = f.readline()
        f.close()

    cursor.close()
    connector.close()

main()

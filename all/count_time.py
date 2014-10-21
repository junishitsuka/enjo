#! /usr/bin/python
# coding: utf-8

import sys, re, MySQLdb

DATA_SET = ['namapo', 'kenketsu', 'spirits']

def get_time(topic):
    data = open('../../data/output/%s_time.csv' % topic, 'r').read()
    data = data.split(',')
    return [ x.rstrip() for x in data ]

def main():
    connector = MySQLdb.connect(db="python", host="localhost", user="root", passwd="", charset="utf8")
    cursor = connector.cursor()

    for topic in DATA_SET:
        data = get_time(topic)

        for d in data[:-1]:
            t = d.split(' ')
            date = t[0].split('/')
            time = t[1].split(':')
            d = date[0] + '-' + date[1] + '-' + date[2] + ' ' + time[0] + ':' + time[1] + ':' + time[2]
            sql = 'INSERT INTO enjo_time (topic, time) VALUE ("%s", "%s")' % (topic, d)
            cursor.execute(sql)
            connector.commit()

    cursor.close()
    connector.close()

main()

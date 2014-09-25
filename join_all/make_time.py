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
            try:
                sql = 'INSERT INTO enjo_basedata (topic, time, tweet_id, content, link, name, retweet_id, retweet_count) VALUE ("%s", "%s", "%s", "%s", "%s", "%s", "%s", %d)' % (topic, d, base[0], base[3], base[5], base[6], base[7], int(base[10]))
                cursor.execute(sql)
                connector.commit()
            except:
                print 'error occured'

            line = f.readline()
        f.close()

    cursor.close()
    connector.close()

main()

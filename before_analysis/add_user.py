#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys

DATA_SET = ['namapo', 'kenketsu', 'spirits']

def main():
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()

    topic = 'spirits'
    # date = ['2012-05-15', '2012-05-16', '2012-05-17', '2012-05-18', '2012-05-19', '2012-05-20', '2012-05-21', '2012-05-22', '2012-05-23', '2012-05-24']
    # date = ['2012-05-21', '2012-05-22', '2012-05-23', '2012-05-24', '2012-05-25', '2012-05-26', '2012-05-27', '2012-05-28', '2012-05-29', '2012-05-30']
    date = ['2014-04-28 01', '2014-04-28 02', '2014-04-28 03', '2014-04-28 04', '2014-04-28 05', '2014-04-28 06', '2014-04-28 07', '2014-04-28 08', '2014-04-28 09', '2014-04-28 10']

    f = open('../../data/output/before_user_%s.csv' % topic, 'w')

    for d in date:
        sql = 'SELECT username FROM enjo_time WHERE topic = "%s" and DATE_FORMAT(time, ' % topic + r'"%Y-%m-%d %H"' + ') = "%s"' % d
        print sql
        cursor.execute(sql)
        users = cursor.fetchall()
        f.write('%s,' % d)
        for u in users:
            f.write('%s,' % u)
        f.write('\n')


    cursor.close()
    connector.close()

main()

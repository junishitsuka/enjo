#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys

DATA_SET = ['namapo', 'kenketsu', 'spirits']

def main():
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()

    for topic in DATA_SET:
        f = open('../../data/output/before_nortuser_%s.csv' % topic, 'r')
        text = f.readlines()
        f.close()
        f = open('../../data/output/before_nortcommunity_%s.csv' % topic, 'w')
        for line in text:
            users = line.split(',')
            community = []
            for u in users[1:-1]:
                sql = 'select %s_communityid from enjo_users where name = "%s"' % (topic, u)
                cursor.execute(sql)
                result = cursor.fetchall()
                community.append(str(result[0][0]))
            f.write('%s,' % users[0])
            f.write('%s' % ','.join(community))
            f.write('\n')

    f.close()
    cursor.close()
    connector.close()

main()

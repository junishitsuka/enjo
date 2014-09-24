#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys

DATA_SET = ['namapo', 'kenketsu', 'spirits']

def get_joinall_user():
    data = open('../../data/output/all_join.csv', 'r').read()
    data = data.split(',')
    return [ x.rstrip() for x in data ]

def main():
    data = get_joinall_user()
    output = {}
    com = []

    topic = 'namapo'

    f = open('../../data/%s/basedata.dat' % topic, 'r')
    line = f.readline()
    while line:
        base = line.split('\t')
        if base[6] in data: com.append(base[1])
        line = f.readline()
    f.close()

    print len(com)
    
    f = open('../../data/output/%s_time.csv' % topic, 'w')
    for c in com:
        f.write(c + ',')
    f.close()

main()

#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys, math

DATA_SET = ['namapo', 'kenketsu', 'spirits']

def get_joinall_user():
    data = open('../../data/output/all_join.csv', 'r').read()
    data = data.split(',')
    return [ x.rstrip() for x in data ]

def main():
    data = get_joinall_user()
    output = {}
    topic = 'spirits'
    com = {}

    community = open('../../data/%s/community_userid.csv' % topic, 'r').readlines()
    for d in data:
        for line in community:
            if line.find(d) >= 0:
                l = line.split(',')
                output.setdefault(l[0], 0)
                output[l[0]] += 1
                com[l[0]] = int(l[1])
    
    f = open('../../data/output/%s_community.csv' % topic, 'w')
    for k,v in sorted(output.items(), key=lambda x: x[1], reverse=True):
        f.write(k + ',' + str(v) + ',' + str(com[k]) + ',' + str(1.0 * v / com[k]) + '\n')
    f.close()

main()

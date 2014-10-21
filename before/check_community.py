#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys, math

DATA_SET = ['namapo', 'kenketsu', 'spirits']

def main():
    output = {}
    com = {}

    for topic in DATA_SET:
        community = open('../../data/output/before_nortcommunity_%s.csv' % topic, 'r').readlines()
        date = ''
        f = open('../../data/output/before_nortcount_%s.csv' % topic, 'w')
        for line in community:
            li = line.split(',')
            date = li[0]
            for l in li[1:]:
                l = l.rstrip()
                output.setdefault(l, 0)
                output[l] += 1
        
            f.write(date + '\n')
            for k,v in sorted(output.items(), key=lambda x: x[1], reverse=True):
                if v >= 3: f.write(k + ',' + str(v) + '\n')
            f.write('\n')
        f.close()
main()

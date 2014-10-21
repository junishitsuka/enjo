#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys, math

DATA_SET = ['namapo', 'kenketsu', 'spirits']

def get_userlists():
    userlists = [[], [], [], []]
    for i in range(len(DATA_SET)):
        data = open('../data/%s/community_userid.csv' % DATA_SET[i], 'r').readlines()
        for j in range(len(data)):
            if j == 0: continue # skip the header line
            d = data[j].split(',')
            for k in range(len(d)):
                if k > 1: userlists[i].append(d[k]) # skip meaningless elements
    return userlists

def main():
    userlists = get_userlists()
    all = set(userlists[0]) & set(userlists[1]) & set(userlists[2])
    f = open('../data/output/all_join.csv', 'w')
    for a in all:
        f.write('%s,' % a.rstrip())
    f.close()

main()

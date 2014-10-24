#! /usr/bin/python
# coding: utf-8

import sys
CLUSTER_MAX_NUMBER = 5 # 5 or 22

def create(f, line, sub = 0):
    fw = open('../../data/output/subcluster5.csv', 'a')
    while line:
        user = line.rstrip().split(',')
        if sub == 0:
            fw.write(user[0] + ',' + user[1] + '\n')
        else:
            fw.write(str(sub) + '_' + user[0] + ',' + user[1] + '\n')
        line = f.readline()
    fw.close()

def allcluster():
    f = open('../../cluster/community/community_propagation_20140530/All/community_userid.csv', 'r')
    line = f.readline()

    count = 0
    while count < CLUSTER_MAX_NUMBER + 1:
        line = f.readline() # ignore the header line
        count += 1

    create(f, line)

def subcluster():
    for i in range(CLUSTER_MAX_NUMBER):
        f = open('../../cluster/community/community_propagation_20140530/Sub/cluster_%s/community_userid.csv' % (i + 1), 'r')
        line = f.readline()
        line = f.readline()
        create(f, line, (i + 1))


def main():
    allcluster()
    subcluster()

if __name__ == '__main__':
    main()

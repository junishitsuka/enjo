#! /usr/bin/python
# coding: utf-8

import sys, glob, re
CLUSTER_MAX_NUMBER = 10000

def create(f, line, sub = 0, subsub = 0, subsubsub = 0):
    fw = open('../../data/output/subsubsubcluster.csv', 'a')
    while line:
        user = line.rstrip().split(',')
        if int(user[1]) < CLUSTER_MAX_NUMBER:
            if sub == 0:
                fw.write(user[0] + ',' + user[1] + '\n')
            elif subsub == 0:
                fw.write(str(sub) + '_' + user[0] + ',' + user[1] + '\n')
            elif subsubsub == 0:
                fw.write(str(sub) + '_' + str(subsub) + '_' + user[0] + ',' + user[1] + '\n')
            else:
                fw.write(str(sub) + '_' + str(subsub) + '_' + str(subsubsub) + '_' + user[0] + ',' + user[1] + '\n')
        line = f.readline()
    fw.close()

def allcluster():
    f = open('../../cluster/community/community_propagation_20140530/All/community_userid.csv', 'r')
    line = f.readline()
    line = f.readline() # skip header
    create(f, line)

def subcluster():
    filelist = glob.glob('../../cluster/community/community_propagation_20140530/Sub/*/community_userid.csv')
    pattern = re.compile(r"/cluster_.*/")
    for file in filelist:
        f = open(file, 'r')
        line = f.readline()
        line = f.readline() # skip header

        cluster = re.search(pattern, file)
        community = cluster.group().replace('/', '').split('_')
        if len(community) == 2:
            create(f, line, int(community[1]))
        elif len(community) == 3:
            create(f, line, int(community[1]), int(community[2]))
        else:
            create(f, line, int(community[1]), int(community[2]), int(community[3]))

def main():
    allcluster()
    subcluster()

if __name__ == '__main__':
    main()

#! /usr/bin/python
# coding: utf-8

import sys
CLUSTER_MAX_NUMBER = 10000

def main():
    f = open('../../cluster/community/community_propagation_20140530/All//community_userid.csv', 'r')
    line = f.readline()
    line = f.readline() # ignore the header line
    while line:
        user = line.rstrip().split(',')
        print int(user[1])
        if (int(user[1]) < CLUSTER_MAX_NUMBER): break # clusterのメンバー数がしきい値より下ならループをbreak
        fw = open('../../cluster/community/community_propagation_20140530/Sub/cluster_%s/userlist.txt' % user[0], 'w')
        for u in user[2:]:
            fw.write(u + '\n')
        fw.close()
        line = f.readline()

if __name__ == '__main__':
    main()

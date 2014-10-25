#! /usr/bin/python
# coding: utf-8

import sys, os
CLUSTER_MAX_NUMBER = 10000

def main():
    for i in range(26):
        f = open('../../cluster/community/community_propagation_20140530/Sub/cluster_%d/community_userid.csv' % (i + 1), 'r')
        line = f.readline()
        line = f.readline() # ignore the header line
        while line:
            user = line.rstrip().split(',')
            print int(user[1])
            if (int(user[1]) < CLUSTER_MAX_NUMBER): break # clusterのメンバー数がしきい値より下ならループをbreak
            os.mkdir('../../cluster/community/community_propagation_20140530/Sub/cluster_%d_%s/' % (i + 1, user[0]))
            fw = open('../../cluster/community/community_propagation_20140530/Sub/cluster_%d_%s/userlist.txt' % (i + 1, user[0]), 'w')
            for u in user[2:]:
                fw.write(u + '\n')
            fw.close()
            line = f.readline()

if __name__ == '__main__':
    main()

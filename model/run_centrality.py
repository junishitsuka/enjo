#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys, os

def main():
    f = open('../../data/output/model/community_list.txt', 'r')
    line = f.readline()

    while line:
        l = line.rstrip()
        os.system('../../library/snap/examples/centrality/centrality -i:../../data/output/model/edge/%s -o:../../data/output/model/cent/%s' % (l, l))
        line = f.readline()

if __name__ == '__main__':
    main()

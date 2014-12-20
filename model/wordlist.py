#! /usr/bin/python
# coding: utf-8

# NodeId Degree  Closeness   Betweennes  EigenVector NetworkConstraint   ClusteringCoefficient   PageRank    HubScore    AuthorityScore

import MySQLdb, sys, os


def get_word(community_list):
    read_file = ''
    target_community = int(community_list[-1])

    if len(community_list) == 1:
        read_file = '../../cluster/community/community_propagation_20140530/All/community_words.csv'
    elif len(community_list) == 2:
        read_file = '../../cluster/community/community_propagation_20140530/Sub/cluster_%s/community_words.csv' % community_list[0]
    elif len(community_list) == 3:
        read_file = '../../cluster/community/community_propagation_20140530/Sub/cluster_%s_%s/community_words.csv' % (community_list[0], community_list[1])
    elif len(community_list) == 4:
        read_file = '../../cluster/community/community_propagation_20140530/Sub/cluster_%s_%s_%s/community_words.csv' % (community_list[0], community_list[1], community_list[2])

    fr = open(read_file, 'r')
    [fr.readline() for i in xrange(target_community)]
    return fr.readline().split(',')[2:-1]


def main():
    f = open('../../data/output/model/community_list.txt', 'r')
    line = f.readline()
    word = []

    while line:
        l = line.rstrip().split('_')
        word.extend(get_word(l))
        line = f.readline()
    f.close()

    fw = open('../../data/output/model/word_list.txt', 'w')
    for w in list(set(word)):
        fw.write('%s\n' % w)
    fw.close()

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()
    main()

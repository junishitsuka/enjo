#! /usr/bin/python
# coding: utf-8

# NodeId Degree  Closeness   Betweennes  EigenVector NetworkConstraint   ClusteringCoefficient   PageRank    HubScore    AuthorityScore

import MySQLdb, sys, os

def insert_db(community, number, label):
    sql = 'insert into all_communities (community_id, member_num, word) values ("%s", %d, "%s")' % (community, int(number), label)
    cursor.execute(sql)
    connector.commit()
    return 0

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
    return fr.readline().split(',')[1:-1]


def getwordlist():
    word = []
    fwr = open('../../data/output/model/word_list.txt', 'r')
    li = fwr.readline()
    while li:
        word.append(li.rstrip())
        li = fwr.readline()
    fwr.close()
    return word

def main():
    f = open('../../data/output/model/community_list.txt', 'r')
    line = f.readline()
    word = getwordlist()

    while line:
        l = line.rstrip().split('_')
        word_list = ['0'] * len(word)
        com = get_word(l)
        com_words = com[1:]
        com_number = com[0]
        for w in com_words:
            index = word.index(w)
            word_list[index] = '1'
        insert_db(line.rstrip(), com_number, ','.join(word_list))
        line = f.readline()

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()
    main()

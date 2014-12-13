#! /usr/bin/python
# coding: utf-8

# NodeId Degree  Closeness   Betweennes  EigenVector NetworkConstraint   ClusteringCoefficient   PageRank    HubScore    AuthorityScore

import MySQLdb, sys, os

def insert_db(community):
    fr = open('../../data/output/model/cent/%s' % community)
    liner = fr.readline()
    while liner:
        t = liner.rstrip().split('\t')
        if t[0][0] != '#':
            t = [float(e) for e in t]
            sql = 'update all_users set com_betweenness=%f, com_closeness=%f, com_eigen=%f, com_pagerank=%f, com_hub=%f, com_authority=%f where node_id = "%s"' % (t[3], t[2], t[4], t[7], t[8], t[9], str(int(t[0])))
            cursor.execute(sql)
        liner = fr.readline()
    connector.commit()
    fr.close()

def main():
    f = open('../../data/output/model/community_list.txt', 'r')
    line = f.readline()

    while line:
        l = line.rstrip()
        insert_db(l)
        line = f.readline()

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()
    main()

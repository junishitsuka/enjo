#! /usr/bin/python
# coding: utf-8

# NodeId Degree  Closeness   Betweennes  EigenVector NetworkConstraint   ClusteringCoefficient   PageRank    HubScore    AuthorityScore

import MySQLdb, sys, os

def insert_db(community):
    fr = open('../../data/output/model/cent/%s' % community)
    liner = fr.readline()
    bet = {}
    while liner:
        t = liner.rstrip().split('\t')
        if t[0][0] != '#':
            bet[str(int(t[0]))] = float(t[3])
        liner = fr.readline()

    if len(bet) > 0:
        min_bet = min(bet.values())
        max_bet = max(bet.values())

        for k,v in bet.items():
            if (max_bet - min_bet) == 0:
                v = 0
            else:
                v = (v - min_bet) / (max_bet - min_bet)
            sql = 'update all_users set com_betweenness=%f, community_id="%s" where node_id = "%s"' % (float(v), str(community), str(int(k)))
            cursor.execute(sql)
        connector.commit()
    fr.close()
    return 0

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

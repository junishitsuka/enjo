#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys, os
from statistics import median

COMMUNITY_LIST = [
    '1_20',
    '1_6_1',
    '1_5_1',
    '1_6_3',
    '1_6_2',
    '1_6_7',
    '1_6_5',
    '1_7_1',
    '5_9',
    '1_6_4',
    '3_4_2',
    '1_4_1',
    '5_1_2',
    '1_6_6',
    '5_2_2',
    '3_20',
    '3_4_3',
    '5_16',
    '5_2_1',
    '5_8',
]

AAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'new']

HEAD = [
    'memberNum',
    'tweetNum',
    'follower',
    'follow',
    'favorite'
]

def get_features(community):
    entry, follower, friend, favorite = [], [], [], []
    for a in AAS:
        sql = 'select a.entryCount, a.follower, a.friend, a.favorite from ishitsuka.all_users as au left join aas_twitter_com.aas_twitter_com_%s as a on a.authorId = au.name where au.cluster_id = "%s" and au.cluster_id2 = "%s" and a.id is NOT NULL'
        subcluster = community.split('_')
        if len(subcluster) == 2:
            sql = sql % (a, subcluster[0], subcluster[1])
        else:
            sql += ' and cluster_id3 = "%s"'
            sql = sql % (a, subcluster[0], subcluster[1], subcluster[2])
        cursor.execute(sql)
        for i in cursor.fetchall():
            entry.append(i[0])
            follower.append(i[1])
            friend.append(i[2])
            favorite.append(i[3])
    return (median(entry), median(follower), median(friend), median(favorite))

def output(result):
    f = open('feature_twitter_median.csv', 'w')
    f.write('community,' + ','.join(HEAD) + '\n')
    for k,v in result.items():
        f.write(k + ',' + ','.join([str(elem) for elem in v]) + '\n')

def main():
    result = {}
    for community in COMMUNITY_LIST:
        result[community] = get_features(community)

    # 出力、とりあえずは標準出力
    output(result)

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()
    main()

#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys, os

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

HEAD = [
    'memberNum',
    'tweetNum',
    'follower',
    'follow',
    'favorite'
]

def get_features(community):
    sql = 'select count(*), (sum(case when a.id is NOT NULL then a.entryCount else 0 end) + sum(case when b.id is NOT NULL then b.entryCount else 0 end) + sum(case when c.id is NOT NULL then c.entryCount else 0 end) + sum(case when d.id is NOT NULL then d.entryCount else 0 end) + sum(case when e.id is NOT NULL then e.entryCount else 0 end) + sum(case when f.id is NOT NULL then f.entryCount else 0 end) + sum(case when g.id is NOT NULL then g.entryCount else 0 end) + sum(case when h.id is NOT NULL then h.entryCount else 0 end) + sum(case when new.id is NOT NULL then new.entryCount else 0 end)) / count(*), (sum(case when a.id is NOT NULL then a.follower else 0 end) + sum(case when b.id is NOT NULL then b.follower else 0 end) + sum(case when c.id is NOT NULL then c.follower else 0 end) + sum(case when d.id is NOT NULL then d.follower else 0 end) + sum(case when e.id is NOT NULL then e.follower else 0 end) + sum(case when f.id is NOT NULL then f.follower else 0 end) + sum(case when g.id is NOT NULL then g.follower else 0 end) + sum(case when h.id is NOT NULL then h.follower else 0 end) + sum(case when new.id is NOT NULL then new.follower else 0 end)) / count(*), (sum(case when a.id is NOT NULL then a.friend else 0 end) + sum(case when b.id is NOT NULL then b.friend else 0 end) + sum(case when c.id is NOT NULL then c.friend else 0 end) + sum(case when d.id is NOT NULL then d.friend else 0 end) + sum(case when e.id is NOT NULL then e.friend else 0 end) + sum(case when f.id is NOT NULL then f.friend else 0 end) + sum(case when g.id is NOT NULL then g.friend else 0 end) + sum(case when h.id is NOT NULL then h.friend else 0 end) + sum(case when new.id is NOT NULL then new.friend else 0 end)) / count(*), (sum(case when a.id is NOT NULL then a.favorite else 0 end) + sum(case when b.id is NOT NULL then b.favorite else 0 end) + sum(case when c.id is NOT NULL then c.favorite else 0 end) + sum(case when d.id is NOT NULL then d.favorite else 0 end) + sum(case when e.id is NOT NULL then e.favorite else 0 end) + sum(case when f.id is NOT NULL then f.favorite else 0 end) + sum(case when g.id is NOT NULL then g.favorite else 0 end) + sum(case when h.id is NOT NULL then h.favorite else 0 end) + sum(case when new.id is NOT NULL then new.favorite else 0 end)) / count(*) from ishitsuka.all_users as au left join aas_twitter_com.aas_twitter_com_a as a on a.authorId = au.name left join aas_twitter_com.aas_twitter_com_b as b on b.authorId = au.name left join aas_twitter_com.aas_twitter_com_c as c on c.authorId = au.name left join aas_twitter_com.aas_twitter_com_d as d on d.authorId = au.name left join aas_twitter_com.aas_twitter_com_e as e on e.authorId = au.name left join aas_twitter_com.aas_twitter_com_f as f on f.authorId = au.name left join aas_twitter_com.aas_twitter_com_g as g on g.authorId = au.name left join aas_twitter_com.aas_twitter_com_h as h on h.authorId = au.name left join aas_twitter_com.aas_twitter_com_new as new on new.authorId = au.name where cluster_id = "%s" and cluster_id2 = "%s" and (a.id is NOT NULL or b.id is NOT NULL or c.id is NOT NULL or d.id is NOT NULL or e.id is NOT NULL or f.id is NOT NULL or g.id is NOT NULL or h.id is NOT NULL or new.id is NOT NULL)'
    subcluster = community.split('_')
    if len(subcluster) == 2:
        sql = sql % (subcluster[0], subcluster[1])
    else:
        sql += ' and cluster_id3 = "%s"'
        sql = sql % (subcluster[0], subcluster[1], subcluster[2])
    cursor.execute(sql)
    return cursor.fetchall()[0]

def output(result):
    f = open('feature_twitter.csv', 'w')
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

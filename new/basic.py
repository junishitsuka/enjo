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
    'number',
    'join',
    'all',
    'tweet',
    'rt',
    'words',
]

def get_number_words(community):
    subcluster = community.split('_')
    before = '_'.join(subcluster[:-1]) # サブクラスタリングされるひとつ前のコミュニティ
    f = open('/home/ishitsuka/enjo/cluster/community/community_propagation_20140530/Sub/cluster_%s/community_words.csv' % before, 'r')
    line = f.readline()
    while line:
        l = line.split(',')
        if l[0] == subcluster[-1]:
            return l[1], ','.join(l[2:]).rstrip()
        else:
            line = f.readline()

def get_join(community, number):
    sql = ''
    subcluster = community.split('_')
    if len(subcluster) == 2:
        sql = 'select count(*) from enjo_users as eu left join all_users as au on au.name = eu.name where au.cluster_id = "%s" and au.cluster_id2 = "%s"' % (subcluster[0], subcluster[1])
    else:
        sql = 'select count(*) from enjo_users as eu left join all_users as au on au.name = eu.name where au.cluster_id = "%s" and au.cluster_id2 = "%s" and au.cluster_id3 = "%s"' % (subcluster[0], subcluster[1], subcluster[2])
    cursor.execute(sql)
    return str(1.0 * cursor.fetchone()[0] / int(number))

def get_all(community, number):
    sql = ''
    subcluster = community.split('_')
    if len(subcluster) == 2:
        sql = 'select count(*) from enjo_users as eu left join all_users as au on au.name = eu.name where eu.spirits_communityid <> 0 and eu.namapo_communityid <> 0 and eu.kenketsu_communityid <> 0 and au.cluster_id = "%s" and au.cluster_id2 = "%s"' % (subcluster[0], subcluster[1])
    else:
        sql = 'select count(*) from enjo_users as eu left join all_users as au on au.name = eu.name where eu.spirits_communityid <> 0 and eu.namapo_communityid <> 0 and eu.kenketsu_communityid <> 0 and au.cluster_id = "%s" and au.cluster_id2 = "%s" and au.cluster_id3 = "%s"' % (subcluster[0], subcluster[1], subcluster[2])
    cursor.execute(sql)
    return str(1.0 * cursor.fetchone()[0] / int(number))

def get_tweet(community, number):
    sql = ''
    subcluster = community.split('_')
    if len(subcluster) == 2:
        sql = 'select count(*) from enjo_basedata as d left join all_users as au on d.name = au.name where au.cluster_id = "%s" and au.cluster_id2 = "%s"' % (subcluster[0], subcluster[1])
    else:
        sql = 'select count(*) from enjo_basedata as d left join all_users as au on d.name = au.name where au.cluster_id = "%s" and au.cluster_id2 = "%s" and au.cluster_id3 = "%s"' % (subcluster[0], subcluster[1], subcluster[2])
    cursor.execute(sql)
    return str(1.0 * cursor.fetchone()[0] / int(number))

def get_rt(community, number):
    sql = ''
    subcluster = community.split('_')
    if len(subcluster) == 2:
        sql = 'select count(*) from enjo_basedata as d left join all_users as au on d.name = au.name where d.retweet_id != "0" and au.cluster_id = "%s" and au.cluster_id2 = "%s"' % (subcluster[0], subcluster[1])
    else:
        sql = 'select count(*) from enjo_basedata as d left join all_users as au on d.name = au.name where d.retweet_id != "0" and au.cluster_id = "%s" and au.cluster_id2 = "%s" and au.cluster_id3 = "%s"' % (subcluster[0], subcluster[1], subcluster[2])
    cursor.execute(sql)
    return str(1.0 * cursor.fetchone()[0] / int(number))

def output(result):
    f = open('feature.csv', 'w')
    f.write('community,' + ','.join(HEAD) + '\n')
    for k,v in result.items():
        f.write(k + ',' + ','.join([v[key] for key in HEAD]) + '\n')

def main():
    result = {}
    for community in COMMUNITY_LIST:
        result[community] = {} # コミュニティごとの結果を入れるdictを初期化
        result[community]['number'], result[community]['words'] = get_number_words(community)
        result[community]['join'] = get_join(community, result[community]['number'])
        result[community]['all'] = get_all(community, result[community]['number'])
        result[community]['tweet'] = get_tweet(community, result[community]['number'])
        result[community]['rt'] = get_rt(community, result[community]['number'])

    # 出力、とりあえずは標準出力
    output(result)

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()
    main()

#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys

AAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'new']

BURST_LIMIT = 5
TOPIC = 'spirits'
FEATURE = 11124 # 18 word: 11106

# base line
# SQL = 'select b.retweet_count, b.content, a.follower, a.friend, a.favorite, a.entryCount from enjo_basedata as b left join aas_twitter_com.aas_twitter_com_%s as a on b.name = a.authorId left join all_users as au on au.name = b.name where retweet_id = "0" and a.authorId is NOT NULL and (b.retweet_count >= ' + str(BURST_LIMIT) +  ' or (b.retweet_count <= 2 and b.retweet_count <> 0)) order by b.retweet_count desc'

# proposal method
SQL = 'select b.retweet_count, b.content, a.follower, a.friend, a.favorite, a.entryCount, au.com_cluster, au.com_degree, au.com_betweenness, au.com_closeness, au.com_eigen, au.com_pagerank, au.com_hub, au.com_authority, c.member_num, c.word from enjo_basedata as b left join aas_twitter_com.aas_twitter_com_%s as a on b.name = a.authorId left join all_users as au on au.name = b.name left join all_communities as c on c.community_id = au.community_id  where topic = "kenketsu" and retweet_id = "0" and a.authorId is NOT NULL and (b.retweet_count >= ' + str(BURST_LIMIT) +  ' or (b.retweet_count <= 2 and b.retweet_count <> 0)) order by b.retweet_count desc'

def get_tweet(sql):
    cursor.execute(sql)
    return cursor.fetchall()

def output(t):
    output = []
    # if t[0] >= BURST_LIMIT:
    #     output.append('1')
    # else:
    #     output.append('0')
    output.append(t[0])
    output.append(str(t[1].count('#')))
    output.append(str(t[1].count('http')))
    output.append(str(t[1].count('@')))
    output.append(str(len(t[1])))
    if t[1] != '' and t[1][0] == '@':
        output.append('1')
    else:
        output.append('0')
    output.extend([str(x) for x in t[2:]])
    return output

def main():
    f = open('train.csv', 'w')
    f.write(','.join(['"%s"' % str(i) for i in xrange(FEATURE)]) + '\n')
    for aas in AAS:
        tweets = get_tweet(SQL % aas)
        for t in tweets:
            f.write('%s\n' % ','.join(output(t)).replace('None', 'NA'))

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()
    main()

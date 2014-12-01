#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys

AAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'new']
SQL = 'select b.retweet_count, b.content, a.follower, a.friend, a.favorite, a.entryCount from enjo_basedata as b left join aas_twitter_com.aas_twitter_com_%s as a on b.name = a.authorId where topic = "spirits" and retweet_id = "0" and a.authorId is NOT NULL and (retweet_count >= 10 or retweet_count <= 2) order by retweet_count desc'

def get_tweet(sql):
    cursor.execute(sql)
    return cursor.fetchall()

def output(t):
    output = []
    if t[0] >= 10:
        output.append('1')
    else:
        output.append('0')
    output.append(str(t[1].count('#')))
    output.append(str(t[1].count('http')))
    output.append(str(t[1].count('@')))
    output.append(str(len(t[1])))
    if t[1][0] == '@':
        output.append('1')
    else:
        output.append('0')
    output.append(str(t[2]))
    output.append(str(t[3]))
    output.append(str(t[4]))
    output.append(str(t[5]))
    return output

def main():
    f = open('train.csv', 'w')
    f.write('Burst,Hashtag,Mention,URL,Length,Reply,Follower,Follow,Favorite,Entry\n')
    for aas in AAS:
        tweets = get_tweet(SQL % aas)
        for t in tweets:
            f.write('%s\n' % ','.join(output(t)))

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()
    main()

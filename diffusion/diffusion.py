#! /usr/bin/python
# coding: utf-8

import MySQLdb
import networkx as nx

TWEETID = '460607471132766208'

class diffusion:
    def __init__(self):
        self.connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
        self.cursor = self.connector.cursor()

    def gettweet(self, tweetid):
        sql = 'SELECT b.name, b.time, b.id, b.tweet_id, u.`spirits_communityid` FROM enjo_basedata as b left join enjo_users_fixed as u on b.name = u.name where retweet_id = %s order by b.time asc limit 100' % tweetid
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getlink(self, name):
        link = []
        sql = 'select name1 from links where name2 = "%s"' % name
        self.cursor.execute(sql)
        link.extend([x[0] for x in self.cursor.fetchall()])
        sql = 'select name2 from links where name1 = "%s"' % name
        self.cursor.execute(sql)
        link.extend([x[0] for x in self.cursor.fetchall()])
        return link

    def getRTchannel(self, name, userlist):
        return list(set(userlist) & set(self.getlink(name)))

    def main(self):
        retweet = self.gettweet(TWEETID)
        userlist = [x[0] for x in retweet]
        firstnode = self.getRTchannel('jyunichidesita', userlist) # 炎上ツイートをRTし、且つそのツイートのユーザーとリンクのあるユーザーの名前のリスト
        print firstnode
        DG = nx.DiGraph()
        for r in retweet:
            print r

if __name__ == '__main__':
    diffusion = diffusion()
    diffusion.main()

#! /usr/bin/python
# coding: utf-8

import MySQLdb
import networkx as nx
import matplotlib.pylab as plt
import datetime

TWEETID = '460607471132766208'

class diffusion:
    def __init__(self):
        self.connector = MySQLdb.connect(db="ishitsuka", host="127.0.0.1", user="ishitsuka", passwd="ud0nud0n", port=3307, charset="utf8")
        self.cursor = self.connector.cursor()

    def gettweet(self, tweetid):
        sql = 'SELECT b.name, b.time, b.id, b.tweet_id, u.`spirits_communityid` FROM enjo_basedata as b left join enjo_users_fixed as u on b.name = u.name where retweet_id = %s order by b.time asc' % tweetid
        self.cursor.execute(sql)
        return {x[0]: x[1:] for x in list(self.cursor.fetchall())}

    def getlink(self, name):
        link = []
        sql = 'select name1 from links where name2 = "%s"' % name
        self.cursor.execute(sql)
        link.extend([x[0] for x in self.cursor.fetchall()])
        sql = 'select name2 from links where name1 = "%s"' % name
        self.cursor.execute(sql)
        link.extend([x[0] for x in self.cursor.fetchall()])
        return link

    def getRTchannel(self, name, userlist, retweet):
        channel = list(set(userlist) & set(self.getlink(name)))
        return [c for c in channel if retweet[c][0] > retweet[name][0]]

    def main(self):
        G = nx.Graph()
        retweet = self.gettweet(TWEETID)
        retweet['jyunichidesita'] = (datetime.datetime(2014, 4, 28, 0, 0, 0),) # 炎上ツイートのユーザーのみの対応
        userlist = retweet.keys()
        # node = self.getRTchannel('jyunichidesita', userlist, retweet) # 炎上ツイートをRTし、且つそのツイートのユーザーとリンクのあるユーザーの名前のリスト
        node = ['reichi062', 'hasiayu', '2nethi', 'NatsukiPydyhgfd', 'soujiro0725', 'Kirokuro', 'Heavymetalskier', 'maiayumio', 'azullechuza', 'hakofuguf']
        while node:
            next = []
            for n in node:
                tmp = self.getRTchannel(n, userlist, retweet)
                next.extend(tmp)
                edges = [(userlist.index(n), userlist.index(x)) for x in tmp]
                G.add_edges_from(edges)
            else:
                node = next

        degree = nx.degree(G)
        close = nx.closeness_centrality(G)
        bet = nx.betweenness_centrality(G)
        eigen = nx.eigenvector_centrality(G)
        f = open('../../data/output/diffusion/centrality.csv', 'w')
        for k,v in sorted(degree.items(), key=lambda x: x[1], reverse=True):
            f.write(str(userlist[k]) + ',' + str(retweet[userlist[k]][0]) + ',' + str(retweet[userlist[k]][3]) + ',' + str(v) + ',' + str(close[k]) + ',' + str(bet[k]) + ',' + str(eigen[k]) + '\n')
        f.close()

        nx.draw(G, node_size=50)
        plt.savefig("../../data/output/diffusion/undirected.png")
        plt.show()

if __name__ == '__main__':
    diffusion = diffusion()
    diffusion.main()

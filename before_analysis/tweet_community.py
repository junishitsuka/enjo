#! /usr/bin/python
# coding: utf-8

import MySQLdb, datetime

class tweetcommunity:
    def __init__(self):
        self.connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
        self.cursor = self.connector.cursor()

    # start から end まで10分間隔で時刻のリストを作成する関数
    def prepare_timelist(self, start = '2014-04-28 11:30:00', end = '2014-04-29 00:00:00'):
        timelist = []
        start_datetime = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        while start_datetime <= end_datetime:
            timelist.append(start_datetime.strftime('%Y-%m-%d %H:%M:%S'))
            start_datetime += datetime.timedelta(minutes=10)
        return timelist

    # SQLでカウントする関数
    def count_community(self, timelist, community, tweet_id = '460607471132766208'):
        dict = {}
        start = timelist.pop(0)
        for time in timelist:
            sql = "select count(*) from enjo_basedata as b left join enjo_users_fixed as u on b.name = u.name where u.spirits_communityid = %d and b.retweet_id = '%s' and time > '%s' and time < '%s' order by time asc;" % (community, tweet_id, start, time)
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()
            dict[time] = ret[0][0]
        return dict

    def main(self):
        timelist = self.prepare_timelist()
        count_community = []
        for i in range(10):
            count_community.append(self.count_community(timelist, i))

        f = open('../../data/output/tweet_community.csv', 'w')
        f.write(','.join([str(x) for x in xrange(11)]))
        for t in timelist:
            f.write(t + ',' + ','.join([str(count_community[x][t]) for x in xrange(10)]) + '\n')
        f.close()

if __name__ == '__main__':
    tweetcommunity = tweetcommunity()
    tweetcommunity.main()

#! /usr/bin/python
# coding: utf-8

import MySQLdb, glob, sys

class userlist:
    def __init__(self):
        self.connector = MySQLdb.connect(db="ishitsuka", host="127.0.0.1", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
        self.cursor = self.connector.cursor()

    def main(self):
        dir = glob.glob('../../cluster/community/community_propagation_20140530/Sub/cluster_*')
        files = [d.split('/').pop() for d in dir]
        for file in files:
            cluster = file.split('_')
            if len(cluster) == 3: # if len(cluster) > 2:
                f = open('../../cluster/community/community_propagation_20140530/Sub/%s/community_userid.csv' % file, 'r')
                line = f.readline()
                line = f.readline() # skip header
                while line:
                    line = line.rstrip().split(',')
                    # print cluster[1] cluster_id
                    # print cluster[2] cluster_id2
                    # print line[0] cluster_id3
                    for m in line[2:]:
                        # sql = ''
                        # if len(cluster) == 3:
                        sql = 'update all_users set cluster_id3 = "%s" where name = "%s"' % (line[0], m)
                        print sql
                        # elif len(cluster) == 4:
                        # sql = 'update all_users set cluster_id4 = %s where name = %s' % (line[0], m)
                        self.cursor.execute(sql)
                    self.connector.commit()
                    line = f.readline()

if __name__ == '__main__':
    userlist = userlist()
    userlist.main()

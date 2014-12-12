#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys

def main():
    f = open('~/enjo/data/output/model/community_list.txt', 'r')
    line = f.readline()

    while line:
        l = line.rstrip().split('_')

        sql = ''
        if len(l) == 1:
            sql = 'select node_id from all_users where cluster_id = "%s"' % l[0]
        if len(l) == 2:
            sql = 'select node_id from all_users where cluster_id = "%s" and cluster_id2 = "%s"' % (l[0], l[1])
        if len(l) == 3:
            sql = 'select node_id from all_users where cluster_id = "%s" and cluster_id2 = "%s" and cluster_id3 = "%s"' % (l[0], l[1], l[2])
        if len(l) == 4:
            sql = 'select node_id from all_users where cluster_id = "%s" and cluster_id2 = "%s" and cluster_id3 = "%s" and cluster_id4 = "%s"' % (l[0], l[1], l[2], l[3])

        cursor.execute(sql)
        node = cursor.fetchall()
        node = [y for x in node for y in x]
        node = '","'.join(node)

        sql = 'select user_id1,user_id2 from all_mentions where user_id1 in ("%s") and user_id2 in ("%s")' % (node, node)
        cursor.execute(sql)
        edges = cursor.fetchall()

        fw = open('~/enjo/data/output/model/edge/%s' % line.rstrip(), 'w')
        for e in edges:
            fw.write('%s\t%s\n' % (e[0], e[1]))
        fw.close()

        line = f.readline()

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()
    main()

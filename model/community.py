#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys

AAS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'new']
SQL = 'select b.retweet_count, b.name, a.cluster_id, a.cluster_id2, a.cluster_id3, a.cluster_id4, a.node_id from enjo_basedata as b left join all_users as a on b.name = a.name where b.topic = "spirits" and b.retweet_id = "0" and (b.retweet_count >= 10 or b.retweet_count <= 2) and a.cluster_id is NOT NULL order by b.retweet_count desc'

def get_tweet(sql):
    cursor.execute(sql)
    return cursor.fetchall()

def main():
    tweets = get_tweet(SQL)
    com = {}
    for t in tweets:
        community = t[2]
        if t[3] is not None:
            community += '_' + t[3]
            if t[4] is not None:
                community += '_' + t[4]
                if t[5] is not None:
                    community += '_' + t[5]
        com.setdefault(community, [])
        com[community].append(t[6])

    for k,v in com.items():
        v = list(set(v))
        for u in v:
            c = 0.0
            cluster = k.split('_')
            sql1,sql2 = '',''
            if len(cluster) == 1:
                sql1 = 'select m.user_id1 from all_mentions as m left join all_users as u on u.node_id = m.user_id1 where u.cluster_id = "%s" and m.user_id2 = "%s"' % (cluster[0], u)
                sql2 = 'select m.user_id2 from all_mentions as m left join all_users as u on u.node_id = m.user_id1 where u.cluster_id = "%s" and m.user_id1 = "%s"' % (cluster[0], u)
            if len(cluster) == 2:
                sql1 = 'select m.user_id1 from all_mentions as m left join all_users as u on u.node_id = m.user_id1 where u.cluster_id = "%s" and u.cluster_id2 = "%s" and m.user_id2 = "%s"' % (cluster[0], cluster[1], u)
                sql2 = 'select m.user_id2 from all_mentions as m left join all_users as u on u.node_id = m.user_id1 where u.cluster_id = "%s" and u.cluster_id2 = "%s" and m.user_id1 = "%s"' % (cluster[0], cluster[1], u)
            if len(cluster) == 3:
                sql1 = 'select m.user_id1 from all_mentions as m left join all_users as u on u.node_id = m.user_id1 where u.cluster_id = "%s" and u.cluster_id2 = "%s" and u.cluster_id3 = "%s" and m.user_id2 = "%s"' % (cluster[0], cluster[1], cluster[2], u)
                sql2 = 'select m.user_id2 from all_mentions as m left join all_users as u on u.node_id = m.user_id1 where u.cluster_id = "%s" and u.cluster_id2 = "%s" and u.cluster_id3 = "%s" and m.user_id1 = "%s"' % (cluster[0], cluster[1], cluster[2], u)
            if len(cluster) == 4:
                sql1 = 'select m.user_id1 from all_mentions as m left join all_users as u on u.node_id = m.user_id1 where u.cluster_id = "%s" and u.cluster_id2 = "%s" and u.cluster_id3 = "%s" and u.cluster_id4 = "%s" and m.user_id2 = "%s"' % (cluster[0], cluster[1], cluster[2], cluster[3], u)
                sql2 = 'select m.user_id2 from all_mentions as m left join all_users as u on u.node_id = m.user_id1 where u.cluster_id = "%s" and u.cluster_id2 = "%s" and u.cluster_id3 = "%s" and u.cluster_id4 = "%s" and m.user_id1 = "%s"' % (cluster[0], cluster[1], cluster[2], cluster[3], u)

            cursor.execute(sql1)
            all_edges1 = cursor.fetchall() # = n

            cursor.execute(sql2)
            all_edges2 = cursor.fetchall() # = n

            n = len(all_edges1) + len(all_edges2) 

            sql = 'update all_users set com_degree = %d where node_id = "%s"' % (n, u)
            cursor.execute(sql)
            connector.commit()

            if n > 1:
                neighbors = [y for x in all_edges1 for y in x]
                neighbors.extend([y for x in all_edges2 for y in x])
                neighbors = '","'.join(neighbors)

                sql = 'select count(*) from all_mentions where user_id1 in ("%s") and user_id2 in ("%s")' % (neighbors, neighbors)
                cursor.execute(sql)
                a = cursor.fetchone()[0] # = n
                c = 2.0 * a / (n * (n - 1))

                sql = 'update all_users set com_cluster = %f where node_id = "%s"' % (c, u)
                cursor.execute(sql)
                connector.commit()

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()
    main()

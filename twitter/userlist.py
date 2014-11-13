#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys

def main():
    sql = 'select cluster_id,cluster_id2,cluster_id3,count(*) from `all_users` as au left join enjo_users as eu on au.name = eu.name where eu.spirits_communityid = "%d" group by au.cluster_id, au.cluster_id2, au.cluster_id3 order by count(*) desc limit 10'
    # sql = 'select cluster_id,cluster_id2,count(*) from `all_users` as au left join enjo_users as eu on au.name = eu.name where eu.spirits_communityid = "%d" group by au.cluster_id, au.cluster_id2 order by count(*) desc limit 10'
    f = open('../../data/output/twitter/spirits_subsubcluster.csv', 'w')
    # f = open('../../data/output/twitter/spirits_subcluster.csv', 'w')
    f.write('cluster_id,count\n')
    for i in range(10):
        jaccard = []
        cursor.execute(sql % (i + 1))
        result = cursor.fetchall()
        enjo_sql = 'select count(*) from enjo_users where spirits_communityid = "%d"' % (i + 1)
        cursor.execute(enjo_sql)
        enjo_count = cursor.fetchone()[0]
        for r in result:
            all_sql = 'select count(*) from all_users where cluster_id = "%s" and cluster_id2 ="%s" and cluster_id3 = "%s"' % (r[0], r[1], r[2])
            cursor.execute(all_sql)
            all_count = cursor.fetchone()[0]
            jaccard.append(1.0 * r[3] / (enjo_count + all_count - r[3])) 
        for j,r in enumerate(result):
            f.write('%s_%s_%s,%d,%f\n' % (r[0], r[1], r[2], r[3], jaccard[j]))
            # f.write('%s_%s,%d\n' % (r[0], r[1], r[2]))
        f.write('\n')

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()
    main()

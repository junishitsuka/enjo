#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys, math

DATA_SET = ['cover', 'namapo', 'kenketsu', 'spirits']
BOTTOM_NUM = 10 # コミュニティの最低人数
LIMIT = 30

def get_community_number(theme, n):
    count = 0
    sql = 'SELECT COUNT(*) AS cnt FROM enjo_users WHERE %s_communityid = %d' % (theme, n)
    cursor.execute(sql)
    count = cursor.fetchall()
    return count[0][0]

def get_jaccard(theme1, num1, theme2, num2):
    numer, denom = 0, 0
    sql = 'SELECT COUNT(*) AS cnt FROM enjo_users WHERE %s_communityid = %d and %s_communityid = %d' % (theme1, num1, theme2, num2)
    cursor.execute(sql)
    numer = cursor.fetchall()
    sql = 'SELECT COUNT(*) AS cnt FROM enjo_users WHERE %s_communityid = %d or %s_communityid = %d' % (theme1, num1, theme2, num2)
    cursor.execute(sql)
    denom = cursor.fetchall()
    return 1.0 * numer[0][0] / denom[0][0]

def main():
    f = open('../data/output/jaccard2.csv', 'w')
    for theme1 in DATA_SET:
        for theme2 in DATA_SET:
            if theme1 == theme2: continue
            num1, n1 = 1, 10000
            while num1 < LIMIT:
                n1 = get_community_number(theme1, num1)
                num2, n2 = 1, 10000
                while num2 < LIMIT:
                    n2 = get_community_number(theme2, num2)
                    jaccard = get_jaccard(theme1, num1, theme2, num2)
                    if jaccard != 0.0: f.write('%s_%d, %s_%d, %f, %d, %d\n' % (theme1, num1, theme2, num2, jaccard, n1, n2))
                    num2 += 1
                num1 += 1

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()

    main()

    cursor.close()
    connector.close()

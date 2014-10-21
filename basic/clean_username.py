#! /usr/bin/python
# coding: utf-8

import MySQLdb

def get_userlist():
    sql = 'select id,name from enjo_users'
    ret = cursor.execute(sql)
    return cursor.fetchall()

def main():
    userlist = get_userlist()
    for user in userlist:
        sql = "UPDATE enjo_users SET name = '%s' WHERE id = %d" % (user[1].rstrip(), user[0])
        print sql
        cursor.execute(sql)
        connector.commit()

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()

    main()

    cursor.close()
    connector.close()

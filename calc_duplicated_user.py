# /usr/bin/python
# coding: utf-8

# 各炎上同士の重複したユーザー数を計算するプログラム
# record数 = 12C2 = 6
# communityは考慮せず、2つの炎上の組み合わせのみで計算

import math, sys

DATA_SET = ['cover', 'namapo', 'kenketsu', 'spirits']

def get_userlists():
    userlists = [[], [], [], []]
    for i in range(len(DATA_SET)):
        data = open('../data/%s/community_userid.csv' % DATA_SET[i], 'r').readlines()
        for j in range(len(data)):
            if j == 0: continue
            d = data[j].split(',')
            for k in range(len(d)):
                if k > 1: userlists[i].append(d[k])
    return userlists

def calc_duplicated_usercount(i, j, userlists):
    count = 0
    for user1 in userlists[i]:
        for user2 in userlists[j]:
            if user1 == user2:
                count += 1
                continue
    return count

def main():
    userlists = get_userlists()
    f = open('../data/output/all_duplicated_usercount.csv', 'w')
    for i in range(len(DATA_SET)):
        for j in range(len(DATA_SET)):
            if i >= j: continue
            f.write('%s,' % DATA_SET[i])
            f.write('%s,' % DATA_SET[j])
            f.write('%s,' % len(userlists[i]))
            f.write('%s,' % len(userlists[j]))
            f.write('%d' % int(calc_duplicated_usercount(i, j, userlists)))
            f.write('\n')

main()

#! /usr/bin/python
# coding: utf-8

f = open('subcluster22.csv', 'r')
community = {}
line = f.readline()
while line:
    t = line.rstrip().split(',')
    community[t[0]] = t[1]
    line = f.readline()
f.close()

sort_com = sorted(community.items(), key = lambda x:int(x[1]), reverse = True)

f = open('subcluster22_sorted.csv', 'w')
for s in sort_com:
    f.write(s[0] + ',' + s[1] + '\n')

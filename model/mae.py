#! /usr/bin/python
# coding: utf-8

# python maeshori.py filename

import sys, os, commands

FILE = sys.argv[1]

def main():
    f = open(FILE, 'r')
    fw = open(FILE + '.na', 'w')
    line = f.readline()
    data = []
    while line:
        if line not in data:
            count = line.count('NA')
            if count == 0:
                fw.write(line)
        data.append(line)
        line = f.readline()

if __name__ == '__main__':
    main()

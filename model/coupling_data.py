#! /usr/bin/python
# coding: utf-8

import sys

DIR = [
    '10',
    '50',
    '100',
    '200',
    'word',
    'com',
    'base'
]
TOPIC = [
    'kenketsu',
    'namapo',
    'spirits'
]
INFILE = '../../data/output/test/%s/%s/train_%d.sampled' # topic dir index
OUTFILE = '../../data/output/test/all/%s/train_%d.sampled' # dir index

def main():
    for d in DIR:
        for index in range(10):
            for t in TOPIC:
                i = index + 1
                f = open(INFILE % (t, d, i), 'r')
                fa = open(OUTFILE % (d, i), 'a')

                line = f.readline()
                if t == 'kenketsu': fa.write(line) # header
                line = f.readline() # skip header

                while line:
                    fa.write('%s' % line)
                    line = f.readline()

if __name__ == '__main__':
    main()

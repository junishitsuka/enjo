#! /usr/bin/python
# coding: utf-8

import sys

INFILE = '../../data/output/test/spirits/50/train_%d.sampled'
OUTFILE_BASE = '../../data/output/test/spirits/base_%d.sampled'
OUTFILE_COM = '../../data/output/test/spirits/com_%d.sampled'

def main():
    for i in range(10):
        f = open(INFILE % (i + 1), 'r')
        line = f.readline()
        fb = open(OUTFILE_BASE % (i + 1), 'w')
        fc = open(OUTFILE_COM % (i + 1), 'w')
        while line:
            t = line.rstrip().split(',')
            fc.write('%s\n' % ','.join(t[:18]))
            fb.write('%s\n' % ','.join(t[:10]))
            line = f.readline()

if __name__ == '__main__':
    main()

#! /usr/bin/python
# coding: utf-8

import sys, os, commands
import numpy as np
from scipy import io, sparse
from scipy.sparse.linalg import svds

NUM = int(sys.argv[2]) # 圧縮次元数
WORD_HEAD = 19
INFILE = sys.argv[1] + '.sampled'
OUTFILE = sys.argv[1] + '.svd'

def make_matrix(f_name):
    f = open(f_name, 'r')
    row = int(commands.getoutput('wc -l %s' % f_name).split(' ')[0])
    line = f.readline()
    line = f.readline() # skip header
    matrix = sparse.lil_matrix((row - 1, len(line.rstrip().split(',')[WORD_HEAD:])))
    count = 0

    while line:
        t = line.rstrip().split(',')
        for i in xrange(len(t[WORD_HEAD:])):
            index = i + WORD_HEAD
            t[index] = t[index].replace('"', '').replace("'", '')
            if t[index] == '1':
                matrix[count, i] = 1
        line = f.readline()
        count += 1
    return matrix

def decomp_dim(num):
    matrix = make_matrix(INFILE)
    return svds(matrix, k=num)[0]

def main():
    result = decomp_dim(NUM)
    f = open(INFILE, 'r')
    fw = open(OUTFILE, 'w')
    line = f.readline()
    line = f.readline() # skip header
    for r in result:
        t = line.split(',')
        print r
        tmp = []
        tmp.extend(t[:18])
        tmp.extend([str(i) for i in r])
        fw.write('%s\n' % ','.join(tmp))
        line = f.readline()

if __name__ == '__main__':
    main()

#! /usr/bin/python
# coding: utf-8

# python maeshori.py filename
# 欠損値処理/ランダムサンプリングスクリプト
# filename.sampledで出力
# 要pandas,numpy

import sys, os, commands
import numpy as np
import pandas as pd

FILE = sys.argv[1]

def random_sampling(plus, minus):
    count = min(len(plus), len(minus))
    if count == len(plus):
        sampler = np.random.permutation(len(minus))
        minus = minus.take(sampler[:count])
    else:
        sampler = np.random.permutation(len(plus))
        plus = plus.take(sampler[:count])
    return plus.append(minus)

def main():
    data = pd.read_csv(FILE)
    data = data.dropna() # 欠損値を除去
    plus = data[data["0"] == 1]
    minus = data[data["0"] == 0]
    data_sampled = random_sampling(plus, minus)
    data_sampled.to_csv('%s.sampled' % FILE, index=False)

if __name__ == '__main__':
    main()

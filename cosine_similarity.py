#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys, math

DATA_SET = ['cover', 'namapo', 'kenketsu', 'spirits']
COMMUNITY_LIMIT = 30

def get_wordlists():
    wordlists = {}

    for theme in DATA_SET:
        wordlists[theme] = []
        data = open('../data/%s/community_words.csv' % theme, 'r').readlines()

        for j in range(COMMUNITY_LIMIT + 1): # due to eliminate header
            if j == 0: continue # skip the header line

            community_words = []
            d = data[j].split(',')

            for k in range(len(d) - 1): # skip line break
                if k > 1: community_words.append(d[k]) # skip meaningless elements
            else:
                wordlists[theme].append(community_words)
    return wordlists

def make_vector(list1, list2):
    vector = {}
    for word in set(list1).union(set(list2)):
        if word in set(list1):
            vector[word] = 1
        else:
            vector[word] = 0
    return vector

def calc_cosine_similarity(v1, v2):
    numerator = sum([v1[c] * v2[c] for c in v1 if c in v2])
    denominator =  math.sqrt(sum(map(lambda x: x * x, v1.values())) * sum(map(lambda x: x * x, v2.values())))
    return float(numerator) / denominator if denominator != 0 else 0

def main():
    wordlists = get_wordlists()

    for theme1 in DATA_SET:
        for theme2 in DATA_SET:
            if theme1 == theme2: continue
            for i in range(COMMUNITY_LIMIT):
                for j in range(COMMUNITY_LIMIT):
                    v1 = make_vector(wordlists[theme1][i], wordlists[theme2][j])
                    v2 = make_vector(wordlists[theme2][j], wordlists[theme1][i])
                    cos = calc_cosine_similarity(v1, v2)
                    f.write('%s_%d, %s_%d, %f\n' % (theme1, i, theme2, j, cos))

if __name__ == '__main__':
    f = open('../data/output/cosine_similarity.csv', 'w')

    main()

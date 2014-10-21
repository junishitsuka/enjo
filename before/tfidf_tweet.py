#! /usr/bin/python
# coding: utf-8

import MySQLdb, sys, MeCab, re, math

DATA_SET = ['namapo', 'kenketsu', 'spirits']
topic = 'namapo'

# date = ['2012-05-15', '2012-05-16', '2012-05-17', '2012-05-18', '2012-05-19', '2012-05-20', '2012-05-21', '2012-05-22', '2012-05-23', '2012-05-24']
date = ['2012-05-21', '2012-05-22', '2012-05-23', '2012-05-24', '2012-05-25', '2012-05-26', '2012-05-27', '2012-05-28', '2012-05-29', '2012-05-30']
# date = ['2014-04-28 01', '2014-04-28 02', '2014-04-28 03', '2014-04-28 04', '2014-04-28 05', '2014-04-28 06', '2014-04-28 07', '2014-04-28 08', '2014-04-28 09', '2014-04-28 10']

# 日付毎のツイートを取得する関数
def get_date_tweet(d):
    tweets = ''
    sql = 'SELECT content FROM enjo_basedata WHERE topic = "%s" and DATE_FORMAT(time, ' % topic + r'"%Y-%m-%d"' + ') = "%s"' % d
    cursor.execute(sql)
    record = cursor.fetchone()

    while record != None:
        word_count = len(record[0])
        # remove url, screen_name of reply
        tmp = re.sub(r'(https?://[a-zA-Z0-9.-/]*)', '', record[0].encode('utf-8'))
        tmp = re.sub(r'@[a-zA-Z0-9_]*', '', tmp)
        tweets += tmp
        record = cursor.fetchone()
    return tweets

def mecab_parse(tweets):
    wordCount = {}
    tagger = MeCab.Tagger()

    word_in_cluster, hash_list = [], []
    # hashタグはパースせずに単語リストへ
    hash_list = re.findall('#(w*[一-龠_ぁ-ん_ァ-ヴー]+|[a-zA-Z0-9]+|[a-zA-Z0-9]w*)', tweets)
    hash_list = ['#' + h for h in hash_list]
    tweets = re.sub('#(w*[一-龠_ぁ-ん_ァ-ヴー]+|[a-zA-Z0-9]+|[a-zA-Z0-9]w*)', '', tweets)
    node = tagger.parseToNode(tweets)
    while node:
        if node.feature.split(',')[0] == '名詞' and int(len(node.surface)) >= 2:
            word_in_cluster.append(node.surface)
        node = node.next
    wordList = word_in_cluster + hash_list

    for word in wordList:
        wordCount.setdefault(word,0)
        wordCount[word]+=1
    return wordCount

# クラスタの中でtf3以下の単語を除去する関数
def remove_few_term(wordCount):
    for i in range(len(wordCount)):
        for k,v in wordCount[i].items():
            if v <= 3: wordCount[i].pop(k)
    return wordCount

def calc_idf(wordCount):
    docNum = int(len(wordCount))
    wordNum = {}
    for i in range(docNum):
        for word in wordCount[i]:
            wordNum.setdefault(word,0)
            wordNum[word]+=1
    for k,v in wordNum.items():
        wordNum[k] = math.log((1.0*docNum/v), math.e)
    return wordNum

def calc_tf(wordCount):
    wordNum = []
    for i in range(len(wordCount)):
        totalCount = 0
        Num = {}
        for j in wordCount[i].values():
            totalCount += j
        for k,v in wordCount[i].items():
            Num[k] = 1.0 * v / totalCount
        wordNum.append(Num)
    return wordNum
   
def calc_tf_idf(tf,idf):
    tf_idfs = []
    for i in range(len(tf)):
        tf_idf = {}
        for word in tf[i].keys():
            tf_idf[word] = tf[i][word] * idf[word]
        tf_idfs.append(tf_idf)
    return tf_idfs

def output(tf_idf):
    f = open('../../data/output/tfidf_%s.txt' % (topic), 'w')
    for i in range(len(tf_idf)):
        f.write(str(i + 1) + '\n')
        output = 0
        for k,v in sorted(tf_idf[i].items(), key=lambda x: x[1], reverse=True):
            if (output != 20):
                f.write(k + ',')
                output += 1
            else:
                break
        f.write('\n')
    f.close()


def main():
    wordCount = []
    for d in date:
        date_tweet = get_date_tweet(d)
        wordCount.append(mecab_parse(date_tweet))
    wordCount = remove_few_term(wordCount)
    idf = calc_idf(wordCount)
    tf = calc_tf(wordCount)
    tf_idf = calc_tf_idf(tf,idf)
    output(tf_idf)
    
if __name__ == '__main__':
    connector = MySQLdb.connect(host='localhost', user='ishitsuka', passwd='ud0nud0n', db='ishitsuka', charset='utf8')
    cursor = connector.cursor()

    main()

    cursor.close()
    connector.close()

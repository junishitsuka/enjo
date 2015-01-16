#coding:utf-8
import csv, MeCab, re, glob, MySQLdb, sys

# return [(単語, ポジネガ, 主観・客観)]
# p: 1.0 e: 0.5 n: 0.0
# 主観: 0.0 客観: 1.0 else 0.5
def set_noun_dic():
    in_file = csv.reader(open('/home/ishitsuka/dictionary/noun_dic.txt',"rU"))
    pne = []
    for line in in_file:
        try:
            if line[1] == 'p': score = 1.0
            elif line[1] == 'e': score = 0.5
            elif line[1] == 'n': score = 0.0
        except: pass

        if (line[2].find('主観') != -1):
            so = 0.0
        elif (line[2].find('客観') != -1):
            so = 1.0
        else: so = 0.5
        pne.append((line[0],score,so))

    return pne

# return [(単語, ポジネガ, 主観・客観)]
# ポジ: 1.0 ネガ: 0.0
# 主観(経験): 1.0 客観: 0.0
def set_verb_dic():
    tfile = open('/home/ishitsuka/dictionary/verb_dic.txt','r')
    vpne = []
    for line in tfile:
        iterator = re.finditer( r'(.*)\t(.*)\t(.*)',line.rstrip(),re.S)
        for match in iterator:
            if ( match.group(1) == "ポジ" ):
                pn = 1.0
            else: pn = 0.0 
            if ( match.group(2) == "経験" ):
                so = 1.0
            else: so = 0.0
            vpne.append((match.group(3),pn,so))
    return vpne

def matching(line):
    pn_score = 0
    num_score = 0
    so_score = 0
    sentiment_words = []

    #用言のマッチング
    tagger = MeCab.Tagger('-F"%f[6] " -U"%m " -E"\n"')
    line = tagger.parse(line)
    line = line.replace('"',' ')
    output = []
    for _vpne in vpne:
        match = re.findall(_vpne[0],line)
        length = len(match)

        i = 0
        if ( length != 0 ):
            while ( i < length ):
                sentiment_words.append(_vpne[0])
                i += 1

        pn_score += _vpne[1] * length
        num_score += length
        so_score += _vpne[2] * length
        line = line.replace(_vpne[0]," ")
    num_decli_score = num_score

    #名詞のマッチング
    tagger = MeCab.Tagger()
    node = tagger.parseToNode(line).next
    keywords = []
    noun_count = 0

    while node:
        parts = node.feature.split(",")[0] 
        if ( parts == "名詞" ):
            noun_count += 1
            keywords.append(node.surface)
        node = node.next

    for token in keywords:
        for _pne in pne:
            if token == _pne[0]:
                sentiment_words.append(_pne[0])
                pn_score += _pne[1]
                so_score += _pne[2]
                num_score += 1

    if num_score != 0:
        pn_rate = float(pn_score)/float(num_score)
        so_rate = float(so_score)/float(num_score)
    else: 
        pn_rate = 0.5
        so_rate = 0.5

    output = [num_score, num_decli_score, pn_rate, so_rate]
    return output, sentiment_words
    
def comment_analysis():
    cursor.execute('SELECT id, content from enjo_basedata where retweet_count >= 1')
    fetch = cursor.fetchall()
    
    for tweet in fetch:
        sentiment_wordList = []
        
        [noun_score,decli_score,pn_rate,so_rate], sentiment_words = matching(tweet[1].encode('utf-8'))
        cursor.execute('update enjo_basedata set pn_rate = %f, so_rate = %f where id = %d' % (pn_rate, so_rate, tweet[0]))
        connector.commit()

if __name__ == '__main__':
    connector = MySQLdb.connect(db="ishitsuka", host="localhost", user="ishitsuka", passwd="ud0nud0n", charset="utf8")
    cursor = connector.cursor()
    pne = set_noun_dic()
    vpne = set_verb_dic()
    print "--------------------"
    print " START TOPICS_TWEET"
    print "--------------------"
    comment_analysis()
    print "--------------------"
    print "\tthe END"
    print "--------------------\n\n"

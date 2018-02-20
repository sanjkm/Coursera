# count_pairs.py
# Process wikipedia articles in pyspark,
# count number of word pairs beginning with narodnaya

from pyspark import SparkConf, SparkContext
from collections import Counter

import re

key_word = "narodnaya"

def parse_article(line):
    try:
        article_id, text = unicode(line.rstrip()).split('\t', 1)
        text = re.sub("^\W+|\W+$", "", text, flags=re.UNICODE)
        words = re.split("\W*\s+\W*", text, flags=re.UNICODE)
        return words
    except ValueError as e:
        return []

# for each word list, returns a list of words that are directly preceded
# by the key_word (global, listed above)
def processRecord (record):

    couple_list = []
    flag = 0
    cnt = Counter()
    for word in record:
        if flag == 1:
            couple_list.append(word.lower())
            cnt[word.lower()] += 1
        flag = 0
        if word.lower() == key_word:
            flag = 1
    return couple_list
    
sc = SparkContext(conf=SparkConf().setAppName("MyApp").setMaster("local"))

wiki = sc.textFile("/data/wiki/en_articles_part/articles-part", 16).map(parse_article)

key_word_pair = wiki.map(processRecord)

key_word_reduce = key_word_pair.reduce(lambda x,y:x+y) # combines RDD into one list

PairWordRDD = sc.parallelize(key_word_reduce)
PairWordCount = PairWordRDD.countByValue() # dictionary, mapping word to count

pair_start = key_word + "_"
for x in sorted(PairWordCount):
    print "%s%s\t%d" % (pair_start,x,PairWordCount[x])

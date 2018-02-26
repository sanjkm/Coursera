# TFreducer.py


import sys
import re
from collections import Counter
import math

reload(sys)
sys.setdefaultencoding('utf-8') # required to convert to unicode

# Prints out the word, article_id, and td*idf for each article_id
# containing the word
def output_word_article (word_article_dict):
    num_articles = len(word_article_dict) # number of articles word appears in
    idf = 1.0 / math.log(1 + num_articles) # article frequency statistic

    for word, article_id in word_article_dict:
        word_count, article_word_count = word_article_dict[(word, article_id)]
        tf = (1.0 * word_count) / article_word_count # term frequency
        tf_idf = tf * idf
        print ("%s\t%s\t%f" % (word, article_id, tf_idf))

delim = '\t'
current_word = None
word_article_dict = {}
for line in sys.stdin:
    word, article_id, word_count, article_word_count = (line.strip()).split(delim)    
    if word != current_word:
        if current_word != None:
            output_word_article (word_article_dict)
        current_word = word
        word_article_dict = {}

    word_count, article_word_count = int(word_count), int(article_word_count)
    word_article_dict[(word, article_id)] = (word_count, article_word_count)

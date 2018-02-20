# Task 2 mapper

import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8') # required to convert to unicode

StopWordsFile = 'stop_words_en.txt'
StopWordsList = []

# Makes a list containing the stop words
with open(StopWordsFile, 'r') as f_stop:
    for line in f_stop:
        StopWordsList.append(line.strip())
f_stop.close()

total_words, stop_words = 0,0
for line in sys.stdin:
    try:
        article_id, text = unicode(line.strip()).split('\t', 1)
    except ValueError as e:
        continue
    words = re.split("\W*\s+\W*", text, flags=re.UNICODE)
    for word in words:
        total_words += 1
        print >> sys.stderr, "reporter:counter:Wiki stats,Total words,%d" % 1
        if word in StopWordsList:
            stop_word_test = 1
        else:
            stop_word_test = 0
        print >> sys.stderr, "reporter:counter:Stop stats,Stop words,%d" % stop_word_test

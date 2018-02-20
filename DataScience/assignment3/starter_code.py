#!/usr/bin/env python

# Dataset location: /data/wiki/en_articles
# Stop words list is in '/datasets/stop_words_en.txt’ file in local filesystem.
# Format: article_id <tab> article_text

import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

for line in sys.stdin:
    try:
        article_id, text = unicode(line.strip()).split('\t', 1)
    except ValueError as e:
        continue
    text = re.sub("^\W+|\W+$", "", text, flags=re.UNICODE)
    words = re.split("\W*\s+\W*", text, flags=re.UNICODE)

    # your code goes here

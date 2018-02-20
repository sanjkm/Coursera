
import sys

reload(sys)
sys.setdefaultencoding('utf-8') # required to convert to unicode

for line in sys.stdin:
    try:
        word, word_count = unicode(line.strip()).split('\t', 1)
    except ValueError as e:
        continue
    word_count = int(word_count)
    print "%d\t%s" % (word_count, word)

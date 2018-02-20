
import sys

reload(sys)
sys.setdefaultencoding('utf-8') # required to convert to unicode

CountDict = {} # key is count, value is list of all words that have that count

for line in sys.stdin:
    try:
        word, word_count = unicode(line.strip()).split('\t', 1)
    except ValueError as e:
        continue
    word_count = int(word_count)
    if word_count in CountDict:
        CountDict[word_count].append(word)
    else:
        CountDict[word_count] = [word]

word_sep = ';'
for word_count in CountDict:
    print "%d\t%s" % (word_count, word_sep.join(CountDict[word_count]))
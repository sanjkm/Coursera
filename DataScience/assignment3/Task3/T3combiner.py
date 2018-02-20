# T3combiner.py
# Takes mapper output as input, counts number of occurrences of
# word and valid_flag, and outputs the results

import sys
import re
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf-8') # required to convert to unicode


def main():
    sep = '\t'
    cnt = Counter()
    
    for line in sys.stdin:
        Nameword, valid, NameCount = (line.strip()).split(sep)
        valid, NameCount = int(valid), int(NameCount)
        cnt[(Nameword, valid)] += NameCount

    CntDict = dict(cnt)
    for Nameword, valid in CntDict:
        print ("%s\t%d\t%d" % (Nameword, valid, CntDict[(Nameword,valid)]))

main()

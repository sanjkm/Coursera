# T3mapper.py

import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8') # required to convert to unicode

# Returns true if a valid name, False if not
# Name valid if starts w uppercase letter, all other letters are lowercase, digits are okay,
# and all characters are alphanumeric
def NameCheck (word):

    digitInt = range(10) 
    digitStr = set([str(s) for s in digitInt])
    
    if word.isalnum() == False: # checks if all alphanumeric characters
        return False
    FirstLetter = word[0]
    if FirstLetter.isalpha() == True and FirstLetter.isupper() == True:
        if len(word) == 1:
            return True 
        if len(word) > 1 and word[1:].islower() == True:
            return True
        for s in word[1:]:
            if s not in digitStr:
                return False
        return True
    return False

def main():
    for line in sys.stdin:
        try:
            article_id, text = unicode(line.strip()).split('\t', 1)
        except ValueError as e:
            continue
        words = re.split("\W*\s+\W*", text, flags=re.UNICODE)
        for word in words:
            if word.isalnum() == False: # No words w non alphanumeric characters
                continue
            if word[0].isalpha() == False: # Only tracking words beginning w letters
                continue

            if NameCheck(word) == True:
                Nameword = word
                valid = 1
            else:
                if len(word) > 1:
                    Nameword = word[0].upper() + word[1:].lower()
                else:
                    Nameword = word[0].upper()
                valid = 0
            print ("%s\t%d\t%d" % (Nameword, valid, 1))
            
main()

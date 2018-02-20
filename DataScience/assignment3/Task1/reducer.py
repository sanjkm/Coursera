
import sys

reload(sys)
sys.setdefaultencoding('utf-8') # required to convert to unicode

# Adds line of word_count and associated words to the WordCountList
# in the correct index such that the list retains reverse sort order in word_count
def AddElementtoList (WordCountList, word_count, words, curr_index):

    if len(WordCountList) == 0: # Insert the first element in the list
        test_index = 0
        WordCountList.append([word_count, words])
        return WordCountList, test_index
        
    if word_count > WordCountList[curr_index][0]:
        test_index = 0
    else:
        test_index = curr_index
        
    while WordCountList[test_index][0] > word_count:
        if test_index < len(WordCountList):
            test_index += 1
        if test_index == len(WordCountList):
            break
    # Now, consider the cases for where to insert this data into the list
    if test_index == len(WordCountList): # Append this data to the list's end
        WordCountList.append ([word_count, words])

    elif WordCountList[test_index][0] == word_count: # Words of this length already exist in the list
        WordCountList[test_index][1] = WordCountList[test_index][1] + words
        
    elif test_index < len(WordCountList): # Insert this data into the list at index test_index
        WordCountList.insert(test_index, [word_count, words])
        
        
    return WordCountList, test_index

WordCountList = []
curr_index = 0
for line in sys.stdin:
    word_sep = ';'
    try:
        word_count, words = unicode(line.strip()).split('\t',1)
        wordList = words.split(word_sep)
    except ValueError as e:
        continue
    word_count = int(word_count)
    WordCountList, curr_index = AddElementtoList (WordCountList, word_count, wordList, curr_index)

for WordCount in WordCountList:
    for word in WordCount[1]:
        print "%s\t%d" % (word, WordCount[0])


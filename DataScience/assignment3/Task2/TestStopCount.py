def main():
    # get the stop words
    stopfile = 'stop_words_en.txt'
    StopWordSet = set()
    with open(stopfile, 'r') as f_stop:
        for line in f_stop:
           StopWordSet.add(line.strip())
    f_stop.close()

    StopCount = 0
    revsortname = "rev_sorted_output.txt"
    dir = "../Task1/"
    revfile = dir + revsortname
    with open(revfile, 'r') as f_rev:
        for line in f_rev:
            word, wordcount = (line.strip()).split('\t')
            if word in StopWordSet:
                StopCount += int(wordcount)
    f_rev.close()

    print StopCount
main()

# decrypt.py
# Program will take in encrypted messages as input, from file
# It will decrypt the final message in the input file and output the
# message.


hexVal = 16

# Ascii code values mapping letters to decimal numbers
upperCaseMin, upperCaseMax, lowerCaseMin, lowerCaseMax = 65,90,97,122


# Opens the input file, places the encrypted messages in a list,
# and returns the list
def getEncryptedMsgs (filename):
    msgList = []
    index = 1
    with open(filename, 'r') as f:
        for line in f:
            if (index % 4) == 3:
                msgList.append(line.rstrip('\n'))
                if msgList[-1][-1] == ' ':
                    msgList[-1].rstrip(' ')
            index+=1
    return msgList

# Takes in two strings of hexadecimal values and outputs their XoR,
# also in the form of hexadecimal string
# First step is to cut the longer string such that each is of the same
# length
def HexStringXor (str1, str2):

    strLen = min(len(str1), len(str2))
    finalStr1 = str1[:strLen]
    finalStr2 = str2[:strLen]

    DecimalXoR = [int(x,hexVal)^int(y,hexVal)
                  for (x,y) in zip(finalStr1, finalStr2)]

    return ''.join([hex(val)[2:] for val in DecimalXoR])

# Takes as input a list of indices, and two encrypted strings
# It will return a subset of that list corresponding to indices that
# may correspond to a space character in one of the strings
# This will be known because the XoR of a space character's ascii code
# with any letter's code will flip the case of that letter

def SpaceCharIndexTest (indexList, str1, str2):
    
    # Each ascii code corresponds to two digits of hexadecimal
    # So an index value of 'x' will correspond to the xth set of 2 characters
    # i.e. character at indices 2*x and 2*x+1

    strXor = HexStringXor (str1, str2)
    if len(indexList) == 0:
        indexList = range(len(strXor)/2)
        
    spaceIndexList = []
    for index in indexList:
        if (2*index+2) > len(strXor):
            break
        hexStr = strXor[2*index:2*index+2]
        testVal = int (hexStr, hexVal)
        
        if (testVal >= upperCaseMin) and (testVal <= upperCaseMax):
            spaceIndexList.append (index)
            continue

        if (testVal >= lowerCaseMin) and (testVal <= lowerCaseMax):
            spaceIndexList.append (index)

        if testVal == 0:
            spaceIndexList.append(index)
            
        # Assuming that any non-space, non-letter will be followed by space    
        if index in spaceIndexList:
            if (index-1) in spaceIndexList:
                spaceIndexList.remove(index-1)

    return spaceIndexList

# For inputs, takes the list of indices of known spaces in message N
# Takes the XoR of the inputted encrypted string N and the encrypted
# target string. At indices where message N is known to contain spaces,
# target string will contain the flipped case of the above XoR
def decryptMsg (SpaceIndexList, encrStrN, encrStrTgt, decrMsg):
    
    strXor = HexStringXor (encrStrN, encrStrTgt)

    for index in SpaceIndexList:

        if index > len(decrMsg):
            break
        
        hexStr = strXor[2*index:2*index+2]
        testVal = int(hexStr, hexVal)
        if testVal == 0:
            decrMsg[index] = ' '
        elif testVal <= upperCaseMax:
            decrMsg[index] = chr(testVal + lowerCaseMin - upperCaseMin)
        else:
            decrMsg[index] = chr(testVal - (lowerCaseMin - upperCaseMin))

    return decrMsg

def main():
    filename = 'msgs.txt'
    msgList = getEncryptedMsgs (filename)
    decrMsg = ['-'] * (len(msgList[-1])/2) # the msg to decrypt

    for i in range(len(msgList)):
        indexList = []
        for j in range(len(msgList)):
            if i == j:
                continue
            indexList = SpaceCharIndexTest (indexList, msgList[i], msgList[j])
        if i == 4:
            print indexList
        if i != len(msgList) - 1:
            decrMsg = decryptMsg (indexList, msgList[i], msgList[-1], decrMsg)
        else:
            for index in indexList:
                decrMsg[index] = ' '
    print ''.join(decrMsg)
    print HexStringXor (msgList[4], msgList[-1])[:16]
    
main()
    

# AESencrypt.py
# Program will take an decrypted string and its key as inputs
# Output is the encrypted string

from CBC import CBCEncrypt, addPadding
from CTR import CTRDecrypt, incrementIVByOne

blockLen = 16 # bytes
hexVal = 16

# Gets the msg and associated data from input file
def getMessageData (filename, delim):
    MessageList = []
    MessageDict = {}
    i = 0
    with open(filename, 'r') as f:
        for line in f:
            x1 = line.rstrip('\n')
            x_line = x1.split(delim)
            mode, key, cipher, IV = x_line[0], x_line[1], x_line[2], x_line[3]
            MessageList.append(cipher)
            MessageDict[cipher, 'mode'] = mode
            MessageDict[cipher, 'key'] = key
            MessageDict[cipher, 'IV'] = IV
    f.close()
    return MessageList, MessageDict


def transAESKey (AESHexKey):
    AESKey = ''
    for i in range(len(AESHexKey)/2):
        TestHex = AESHexKey[2*i:2*i+2]
        AESKey += chr(int(TestHex, hexVal))
    return AESKey

# Takes list containing transformed cipher text (into bytes) as input
# Returns IV value (prepended to CT) and a list
# containing each cipher text block, based on block size (in bytes)
# IV length is assumed to be equal to blockLen
def createMessageBlocks (messageList):

    messageBlockList = []
    for i in range(0, len(messageList)/blockLen):
        messageBlockList.append (messageList[blockLen*i:blockLen*(i+1)])
        
    if len(messageList) % blockLen != 0:
        messageBlockList.append(messageList[(len(messageList)/blockLen)*blockLen:])
    return messageBlockList

# Takes msg text in byte mode and returns same msg text corresponding
# to hex mode
def transformMessageText (msgText):
    
    transMessageText = '';
    for i in range (len(msgText)):
        TestHex = hex(ord(msgText[i]))[2:]
        transMessageText += TestHex
    return transMessageText


def main():

    InputFile = 'messages.txt'
    delim = ','
    MessageList, MessageDict = getMessageData (InputFile, delim)
    
    for msgT in MessageList:
        AESMode = MessageDict[msgT, 'mode']
        AESHexKey = MessageDict[msgT, 'key']
        IVHex = MessageDict[msgT, 'IV']

        messageBlockList = createMessageBlocks (msgT)
        AESKey = transAESKey (AESHexKey)
        IV = transAESKey (IVHex)
        
        if AESMode == 'CBC':
            msgBlockList = addPadding (messageBlockList, blockLen)

            cipherBlockList = CBCEncrypt (AESKey, IV, msgBlockList)
            cipher = transformMessageText(''.join(cipherBlockList))            
            print IVHex + cipher
        elif AESMode == 'CTR':
            msgBlockList = messageBlockList
            cipherBlockList = CTRDecrypt (AESKey, IV, msgBlockList)
            cipher = transformMessageText(''.join(cipherBlockList))            
            print IVHex + cipher
            
main()

# HexAsciiFns.py

hexVal = 16
# Takes in string in hex form and outputs it in byte form
def transHexKey (AESHexKey):
    AESKey = ''
    for i in range(len(AESHexKey)/2):
        TestHex = AESHexKey[2*i:2*i+2]
        AESKey += chr(int(TestHex, hexVal))
    return AESKey

# Takes msg text in byte mode and returns same msg text corresponding
# to hex mode
def transformMessageText (msgText):
    
    transMessageText = '';
    for i in range (len(msgText)):
        TestHex = hex(ord(msgText[i]))[2:]
        if len(TestHex) == 1:
            TestHex = '0' + TestHex
        transMessageText += TestHex
    return transMessageText


# CBC.py
# Functions that facilitate AES encryption via cyber block chaining

from Crypto.Cipher import AES

def xor_strings (str1, str2):
    return "".join(chr(ord(a)^ord(b)) for a,b in zip(str1, str2))

def CBCDecrypt (AESKey, IV, cipherBlockList):
    obj = AES.new (AESKey, AES.MODE_ECB)
    msgBlockList = []
    
    for i in range(len(cipherBlockList)):
        TestCipher = ''
        for CipherByte in cipherBlockList[i]:
            TestCipher += CipherByte
        initDecrypt = obj.decrypt(TestCipher)
        for j in range(len(initDecrypt)):
            if i == 0:
                pass
        if i == 0:
            msgBlockList.append (xor_strings(IV, initDecrypt))
        else:
            msgBlockList.append(xor_strings(PrevTestCipher, initDecrypt))
        PrevTestCipher = TestCipher
        
    return msgBlockList

def CBCEncrypt (AESKey, IV, msgBlockList):
    obj = AES.new (AESKey, AES.MODE_ECB)
    cipherBlockList = []
    
    for i in range(len(msgBlockList)):
        TestMsg = ''
        for MsgByte in msgBlockList[i]:
            TestMsg += MsgByte

        if i == 0:
            initEncrypt = obj.encrypt(xor_strings(IV, TestMsg))
            cipherBlockList.append (initEncrypt)
        else:
            initEncrypt = obj.encrypt(xor_strings(PrevTestCipher, TestMsg))
            cipherBlockList.append (initEncrypt)
        PrevTestCipher = initEncrypt
        
    return cipherBlockList



def cutPadding (msgBlockList):
    lastBlock = msgBlockList[-1]
    cut_num = ord(lastBlock[-1])
    cutBlock = lastBlock[:-1*cut_num]
    del msgBlockList[-1]
    msgBlockList.append(cutBlock)
    return msgBlockList

def addPadding (msgBlockList, blockLen):
    lastBlock = msgBlockList[-1]
    if len(lastBlock) < blockLen: # pad message with suitable number of terms
        PadTerm = blockLen - len(lastBlock)
        newLastBlock = lastBlock + ''.join([chr(PadTerm)]*PadTerm)
        del msgBlockList[-1]
        
    elif len(lastBlock) == blockLen:
        PadTerm = blockLen
        newLastBlock = [chr(PadTerm)]*PadTerm
        
    msgBlockList.append(newLastBlock)
    return msgBlockList

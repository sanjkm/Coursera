# CTR.py
# Functions for AES encryption using randomized counter mode

from Crypto.Cipher import AES
hexVal = 16
ByteVal = 256

def xor_strings (str1, str2):
    return "".join(chr(ord(a)^ord(b)) for a,b in zip(str1, str2))

def CTRDecrypt (AESKey, IV, cipherBlockList):
    obj = AES.new (AESKey, AES.MODE_ECB)
    msgBlockList = []
    IVinc = IV
    for cipherBlock in cipherBlockList:
        encrIV = obj.encrypt (''.join(IVinc))
        if len(cipherBlock) < len(encrIV): 
            encrIV = encrIV[:len(cipherBlock)]
        msgBlockList.append(xor_strings (cipherBlock, encrIV))
        IVinc = incrementIVByOne (IVinc)
    return msgBlockList

# Add 1 to IV and return in byte mode
def incrementIVByOne (IV):
    
    newCharList = ''
    CurrIndex = 1
    newCharVal = 0
    
    while (newCharVal % ByteVal) == 0:
        if CurrIndex > 1:
            newCharList = '0' + newCharList
        lastChar = IV[-1*CurrIndex]
        newCharVal = ord(lastChar) + 1
        CurrIndex += 1
        if CurrIndex > len(IV):
            break

    newCharList = chr(newCharVal) + newCharList
    IVLen = len(IV)
    IVinc = IV[:(IVLen-len(newCharList))] + ''.join(list(newCharList))
    return IVinc
    
        

import urllib2
import sys
sys.path.append ('../')

from HexAsciiFns import transHexKey, transformMessageText

TARGET = 'http://crypto-class.appspot.com/po?er='
MaxByteNum = 255

#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:          
            # print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding


# Gets the cipher text from inputted file
def getCipherText (filename):
    with open(filename, 'r') as f1:
        for line in f1:
            x_str = (line.rstrip('\n')).rstrip(' ')
            break
    f1.close()
    return x_str

# Runs through the guesses for the Byte Value between string CipherPrefix
# and string CipherSuffix
# Concatenated string is converted to hex, and then sent to the server
# to check if valid (good padding). Guess value that returns True is returned
def GuessByteValue (ByteCipherPrefix, ByteCipherSuffix,
                    ByteCipherShift, ByteCipherText, KnownVals):
    
    po = PaddingOracle()
    PadNum = len(ByteCipherShift)
    CipherShiftVals = [ord(x) for x in ByteCipherShift]
    PadList = [PadNum] * PadNum

    test_g = MaxByteNum
    noerror = 0
    
    for g in range(MaxByteNum):
        GuessList = [g] + list(KnownVals)
        InitXor = [x[0]^x[1] for x in zip (CipherShiftVals, PadList)]
        FinalXor = [x[0]^x[1] for x in zip (InitXor, GuessList)]
        NewByteCipherShift = [chr(x) for x in FinalXor]
        TestHexText = transformMessageText (list(ByteCipherPrefix) +
                                            NewByteCipherShift +
                                            list(ByteCipherSuffix))

        # if the test text is exactly equal to the original cipher text,
        # then the web server will not throw an error, as this is a
        # valid URL. This code byte accounts for that case
        if len(GuessList) == len(PadList):
            for i in range(len(GuessList)):
                if GuessList[i] != PadList[i]:
                    break
                if i == (len(GuessList) - 1):
                    noerror = 1
                    alt_g = g
                
        if po.query (TestHexText) == True:
            return g

    if noerror == 1: # web server did not throw an error for a value of g
        return alt_g

    

if __name__ == "__main__":
    filename = 'cipher.txt'
    CipherText = getCipherText (filename)
    
    ByteCipherText = transHexKey (CipherText)
    BlockSize = 16  # AES is used here in 16 byte blocks
    
    KnownVals = []
    
    for ByteNum in range(len(ByteCipherText) - BlockSize):

        PadNum = (ByteNum % BlockSize) + 1
        EndIndex = len(ByteCipherText) - BlockSize - BlockSize * (ByteNum/16)
        BegIndex = EndIndex - PadNum
        
        g = GuessByteValue (ByteCipherText[:BegIndex],
                            ByteCipherText[EndIndex:EndIndex+BlockSize],
                            ByteCipherText[BegIndex:EndIndex],
                            CipherText,
                            KnownVals[:(PadNum-1)])        
        KnownVals = [g] + KnownVals
        
    PadAmt = KnownVals[-1]
    DecryptedMsg = [chr(x) for x in KnownVals[:-1*PadAmt]]
    print ''.join(DecryptedMsg)

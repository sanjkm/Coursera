# VideoHash.py
# Program will take a video file as input
# It takes 1024 byte chunks of the file, starting from the end.
# It calculates the hash value
# of a chunk using SHA-256. Then, this hash is appended to the previous chuck,
# which is then hashed, and appended to the previous block until the
# beginning of the file

from Crypto.Hash import SHA256
import os

# Takes file, makes a list containing blocks of the whole file. Each block
# contains 1024 bytes, except the final block
def makeFileBlocks (filename):
    BlockSize = 1024
    f1 = open(filename, 'r')
    block = f1.read(BlockSize)
    blockList = []
    while len(block) == BlockSize:
        blockList.append(block)
        block = f1.read(BlockSize)

    if len(block) > 0:
        blockList.append(block)
    print len(blockList[-1])
    return blockList

# Returns SHA256 hash of a block of the file
def CalcBlockHash (MsgBlock):
    m = SHA256.new()
    m.update (MsgBlock)
    return m.digest()

# Takes input as bytes and returns in hex
def transformMessageText (msgText):
    transMessageText = '';
    
    for i in range (len(msgText)):
        TestHex = hex(ord(msgText[i]))[2:]
        if len(TestHex) == 1:
            TestHex = '0' + TestHex
        transMessageText += TestHex
    return transMessageText



def main():
    inputFile = '6.1.intro.mp4_download'
    BlockSize = 1024
    f1 = open(inputFile, 'r')
    
    FileSize =  os.path.getsize(f1.name)
    NumBlocks = FileSize / BlockSize
    if FileSize % BlockSize > 0:
        NumBlocks += 1
        lastBlockSize = FileSize % BlockSize
    else:
        lastBlockSize = BlockSize

    ReadBlocks = 0
    while ReadBlocks < NumBlocks:
        f1.seek (-1*(lastBlockSize + ReadBlocks * BlockSize),2)
        if ReadBlocks == 0:
            CurrBlock = f1.read (lastBlockSize)
        else:
            CurrBlock = f1.read (BlockSize)
            CurrBlock += hashStr
        m = SHA256.new()
        m.update(CurrBlock)
        hashStr = m.digest()
        ReadBlocks += 1

    f1.close()
    print transformMessageText (hashStr)
    
main()
        
    

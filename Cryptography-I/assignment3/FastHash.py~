# VideoHash.py
# Program will take a video file as input
# It takes 1024 byte chunks of the file, starting from the end.
# It calculates the hash value
# of a chunk using SHA-256. Then, this hash is appended to the previous chuck,
# which is then hashed, and appended to the previous block until the
# beginning of the file

from Crypto.Hash import SHA256

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
    BlockList = makeFileBlocks (inputFile)
    
    hashString = CalcBlockHash (BlockList[-1])
    del BlockList[-1]
    
    while len(BlockList) > 0:
        BlockList[-1] += hashString
        hashString = CalcBlockHash (BlockList[-1])
        del BlockList[-1]

    print transformMessageText (hashString)

main()
        
    

# dlog.py
# Calculate the discrete log of the h base g modulo prime p
# p,g, and h are from the inputted file

from numbthy import power_mod, inverse_mod
import time

# Gets input values from file
def get_values (filename):
    ValList = []
    with open(filename, 'r') as f1:
        for line in f1:
            ValList.append(int(line.rstrip('\n')))
    f1.close()
    return ValList[0], ValList[1], ValList[2]

def f1 (p, g, x0, b):
    return power_mod (g, (x0*b), p)

# Calculates value of h / g^x1 (mod p)

def f2 (p, g, h, x1):
    denom = power_mod (g, x1, p)

    return (h * inverse_mod(denom,p)) % p


# Builds dictionary containing mapping of f2(i) to i
def buildHashMapf2 (maxVal, p, g, h):
    f2HashDict = {}

    for i in range(maxVal):
        f2HashDict[f2(p,g,h,i)] = i
    return f2HashDict

# Evaluates values of f1 looking for a value contained in f2HashDict
# If value is found, returns the f1 input and the f2 dictionary hash value
def findf1ValMatch (maxVal, p, g, h, f2HashDict):
    for i in range(maxVal):
        testVal =  f1 (p, g, i, maxVal)
        if testVal in f2HashDict:
            return i, f2HashDict[testVal]
    return None

# dLog = x0*B + x1
def calcDLog (x0, x1, B):
    return (x1 + x0 * B)

def main():
    StartTime = time.time()
    filename = 'inputs.txt'
    p, g, h = get_values (filename)
    B = (2 ** 20)
    f2HashDict = buildHashMapf2 (B, p, g, h)
    x0, x1 = findf1ValMatch (B, p, g, h, f2HashDict)
    print calcDLog (x0,x1,B)
    print time.time() - StartTime
main()

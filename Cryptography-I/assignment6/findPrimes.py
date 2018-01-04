# findPrimes.py
import sys
sys.path.append ("../")

from numbthy import power_mod, inverse_mod, is_prime
import decimal
decimal.getcontext().prec = 350
from HexAsciiFns import transHexKey


# Gets the modulus associated with the four problems in the assigment
# Moduli are large integers located on a separate line of the input file
def getModulus (filename):
    ModList = []
    with open(filename, 'r') as f1:
        for line in f1:
            ModList.append(int(line.rstrip('\n')))
    f1.close()
    return ModList

# Factor N given that p,q are within 2*(N**0.25)
def problem1 (N):
    A = decimal.Decimal(N).sqrt()
    A = int(A) + 1
    x = decimal.Decimal(A*A - N).sqrt()
    p,q = A - x, A + x

    if p*q == decimal.Decimal(N):
        return p, q
    else:
        print "Problem 1 Error"
        return 0
    
# Factor N given that p,q are within (2^11)*(N^0.25) of each other
def problem2 (N):
    N = decimal.Decimal(N)
    
    # Use this routine to find A value that fits for N
    A = int(N.sqrt())+1
    index = 1
    maxdiff = 2**19 # A - sqrt(N) < 2 ** 19
    while (index < maxdiff):
        x2 = A*A - N
        x = int(x2.sqrt())
        if x*x == x2:
            p,q = A - x, A + x
            if (p*q == N):
                if is_prime(p) == True and is_prime(q) == True:
                    return p
        index+=1
        A+=1
    print "No solution"
    return 0, 0

# Returns the two solutions to the standard quadratic formula
def quadraticFormula (a,b,c):
    A,B,C = decimal.Decimal(a), decimal.Decimal(b), decimal.Decimal(c)
    radical = (B*B - 4 * A * C).sqrt()
    if radical < 0:
        print "Complex solutions, not valid"
        exit(1)
    return ((-1*B + radical) / (2 * A), (-1*B - radical) / (2 * A))

# Factors N given that abs(3p-2q) < N^0.25
# Can show that (3p+2q)/2 must be v close to sqrt(6*N) and use quadratic
# formula to solve
def problem3 (N):
    N = decimal.Decimal(N)
    A = int(2 * decimal.Decimal (6 * N).sqrt()) + 1

    p1,p2 = quadraticFormula (3,-1*A, 2*N)
    q1,q2 = N / p1, N / p2
 
    if int(p1) == p1 and int(q1) == q1 and p1 < q1:
        return p1

    if int(p2) == p2 and int(q2) == q2 and p2 < q2:
        return p2

# Gets cipher text from input file
def getCipher (cipherfile):
    with open(cipherfile, 'r') as cfile:
        for line in cfile:
            cipherVal = int(line.rstrip(' '))
    cfile.close()
    return cipherVal
# Given the Cipher text, encryption exponent, and factor primes, this
# calculates the decryption exponent and returns the decrypted cipher text
def DecryptCipher (CipherVal, EncExp, p1, q1):
    DecExp = inverse_mod (EncExp, (p1-1)*(q1-1))
    MsgVal = power_mod (CipherVal, DecExp, p1*q1)

    return MsgVal

# Given a PKCS1.5 encryption of a message, this function decrypts the message
# given the prime factors of N along with the Encryption exponent used in the
# RSA encryption
def problem4 (N, cipherfile, EncExp, p1_soln, q1):
    CipherVal = getCipher (cipherfile)
    p1 = p1_soln
    
    MsgVal = DecryptCipher (CipherVal, EncExp, p1, q1)
    HexMsgStr = hex(MsgVal)
    
    SeparatorStr = '00'
    beg_index = HexMsgStr.find (SeparatorStr)
    if beg_index == -1:
        "Error - did not find string separator"
    MsgText = HexMsgStr[beg_index+2:] # Gets the string after the sep string

    return transHexKey (MsgText)
    
    
def main():
    filename = 'Modinputs.txt'
    ModList = getModulus (filename)
    p1_soln, q1 = problem1 (ModList[0])
    p2_soln = problem2 (ModList[1])
    p3_soln = problem3 (ModList[2])

    EncExp = 65537 # given
    cipherfile = 'cipher.txt'
    p4_soln = problem4 (ModList[3], cipherfile, EncExp, int(p1_soln), int(q1))

    print p1_soln
    print p2_soln
    print p3_soln
    print p4_soln

main()

# Large Prime Generation for RSA
import random
from bitstring import Bits


# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
					31, 37, 41, 43, 47, 53, 59, 61, 67,
					71, 73, 79, 83, 89, 97, 101, 103,
					107, 109, 113, 127, 131, 137, 139,
					149, 151, 157, 163, 167, 173, 179,
					181, 191, 193, 197, 199, 211, 223,
					227, 229, 233, 239, 241, 251, 257,
					263, 269, 271, 277, 281, 283, 293,
					307, 311, 313, 317, 331, 337, 347, 349]


fermat_primes = [65537, 257, 17, 5, 3]

def nBitRandom(n):
	return random.randrange(pow(2, n-1) + 1, pow(2, n) - 1)


def getLowLevelPrime(n):
	
	while True:
		# Obtain a random number
		prime = nBitRandom(n)

		for divisor in first_primes_list:
			if prime % divisor == 0 and divisor**2 <= prime:
				break
		else:
			return prime


def isMillerRabinPassed(mrc):
	'''Run 20 iterations of Rabin Miller Primality test'''
	maxDivisionsByTwo = 0
	ec = mrc-1
	while ec % 2 == 0:
		ec >>= 1
		maxDivisionsByTwo += 1
	assert(2**maxDivisionsByTwo * ec == mrc-1)

	def trialComposite(round_tester):
		if pow(round_tester, ec, mrc) == 1:
			return False
		for i in range(maxDivisionsByTwo):
			if pow(round_tester, 2**i * ec, mrc) == mrc-1:
				return False
		return True

	# Set number of trials here
	numberOfRabinTrials = 20
	for i in range(numberOfRabinTrials):
		round_tester = random.randrange(2, mrc)
		if trialComposite(round_tester):
			return False
	return True

def gen_prime(n):
    while True: 
        prime_candidate = getLowLevelPrime(n)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            return prime_candidate
            

def gcd(a,b):
    while True:
        if a == 0:
            return b
        else:
            b = b % a
            a,b = b,a


def keys():
    p = gen_prime(1024)
    q = gen_prime(1024)

    n = p*q
    phi = (p-1)*(q-1)

    for i in fermat_primes:
        if gcd(i, phi) == 1:
            e = i
            break

    # print(e)
    d = pow(e, -1, phi)
    # print(d)
    return (e, n), (d, n)

def enc(e, n, m):
    m = int(m, 2)
    c = pow(m, e, n)
    
    c = '{:08b}'.format(c)
    return(c)
    

def dec(d, n, c):
    c = int(c, 2)
    m = pow(c, d, n)
    
    m = '{:08b}'.format(m)
    m = (8 - (len(m) % 8)) * "0" + m
    return(m)
    pass

(e, n), (d, n) = keys()
m = "01100001011000100110001101100100"
c = enc(e, n, m)
print(c)
m = dec(d, n, c)
print(m)

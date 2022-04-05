from random import randint
from sympy import *
from math import log2

def xor_lists(bigger, lowwer):

	bigger = bigger.copy()
	print(bigger)
	print(lowwer)
	for i in range(len(lowwer)):
		bigger[i] = (bigger[i] + lowwer[i]) % 2
	print(bigger)
	return bigger

def blume_goldwasser_e(n, m):
	m = list(map(int, list(bin(m)[2:])))
	r = randint(2, n - 2)
	x0 = pow(r, 2, n)

	x, b = [x0], [int(bin(x0)[-1])]
	for i in range(len(m) - 1):
		x.append(pow(x[-1], 2, n))
		b.append(int(bin(x[-1])[-1]))

	return (xor_lists(m, b), pow(x[-1], 2, n))

def blume_goldwasser_d(p, q, c):
	y = c[1]
	c = c[0]
	rp, rq = pow(y, pow((p + 1) // 4, len(c)), p), pow(y, pow((q + 1) // 4, len(c)), q)
	x0 = (q * pow(q, -1, p) * rp + p * pow(p, -1, q) * rq) % n

	x, b = [x0], [int(bin(x0)[-1])]
	for i in range(len(c) - 1):
		x.append(pow(x[-1], 2, n))
		b.append(int(bin(x[-1])[-1]))

	return xor_lists(c, b)

if __name__ == '__main__':
	p, q = randprime(2**15, 2**16), randprime(2**15, 2**16)
	while not (p % 4 == 3 and q % 4 == 3):
		p, q = randprime(2**15, 2**16), randprime(2**15, 2**16)
	n = p * q
	m = 123456789
	#m = 5
	#p = 31
	#q = 23
	#n = 713
	
	c = blume_goldwasser_e(n, m)
	print(m)
	print(c)
	mn = blume_goldwasser_d(p, q, c)
	print(int("".join(list(map(str, mn))), 2))
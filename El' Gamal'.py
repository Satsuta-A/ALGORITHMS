from sympy import *
from random import randint

def el_gamal(p, M):
	g = primitive_root(p)
	x = randint(2, p - 1)
	y = pow(g, x, p)
	k = randint(2, p - 1)
	while gcd(k, p - 1) != 1:
		k = randint(2, p - 1)
	C = M * pow(y, k, p) % p 
	a = pow(g, k, p)
	print(C)
	#-->
	M = C * pow(a, p - 1 - x, p) % p
	return M

if __name__ == '__main__':
	#phi = totient
	#lambd = reduced_totient
	#multiplicative_order = n_order
	p = nextprime(10**15+1000*12)
	M = randint(2, p - 1)
	print(M)
	print(el_gamal(p, M))
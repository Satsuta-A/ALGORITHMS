from random import randint
from sympy import *

def mikally_goldwasser_e(n, m, y):
	m = list(map(int, list(bin(m)[2:])))
	x = [randint(0, n - 1) for i in range(len(m))]
	c = []
	for i in range(len(m)):
		if m[i] == 0:
			c.append(pow(x[i], 2, n))
		else:
			c.append(y * pow(x[i], 2, n) % n)
	return c

def mikally_goldwasser_d(p, q, c):
	m = []
	for i in range(len(c)):
		if legendre_symbol(c[i], p) == 1 and legendre_symbol(c[i], q) == 1:
			m.append(0)
		else:
			m.append(1)
	return m


if __name__ == '__main__':
	p, q = randprime(2**15, 2**16), randprime(2**15, 2**16)
	n = p * q
	y = randint(2, n - 1)
	while jacobi_symbol(y, n) == 0 or legendre_symbol(y, p) == 1 or legendre_symbol(y, q) == 1:
		y = randint(2, n - 1)
	m = 123456789
	print(list(map(int, list(bin(m)[2:]))))
	c = mikally_goldwasser_e(n, m, y)
	print(c)
	m = mikally_goldwasser_d(p, q, c)
	print(m)


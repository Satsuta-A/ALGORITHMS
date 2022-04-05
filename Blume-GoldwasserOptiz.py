from random import randint
from sympy import *
from math import log2, ceil

def parting(xs, parts):
    part_len = ceil(len(xs)/parts)
    return [xs[part_len*k:part_len*(k+1)] for k in range(parts)]

def xor_lists(bigger, lowwer):
	bigger = bigger.copy()
	"""	print(bigger)
	print(lowwer)"""
	for i in range(len(lowwer)):
		bigger[i] = (bigger[i] + lowwer[i]) % 2
	#print(bigger)
	return bigger

def blume_goldwasser_e(n, m):
	m = list(map(int, list(bin(m)[2:])))
	r = randint(2, n - 1)
	#r = 36
	h = int(log2(int(log2(n))))
	#h = 3
	#print(len(m))
	t = len(m) // h
	x0 = pow(r, 2, n)
	hell = t * h
	mh = m[hell:]
	m = m[:hell]
	m = parting(m, t)
	c = []
	for i in range(-1, t - 1):
		x = pow(x0, 2, n)
		x0 = x
		b = list(map(int, list(bin(x)[2:])))[len(bin(x)) -2 - h:]
		c.append(xor_lists(m[i + 1], b))
	c.append(mh)
	"""print('m', m + [mh])
				print('c', c)
				print(pow(x0, 2, n))"""
	return (c, pow(x0, 2, n))

def blume_goldwasser_d(p, q, c):
	n = p * q
	y = c[1]
	c = c[0]
	t = len(c) - 1
	u, v = pow(y, pow((p + 1) // 4, t + 1, p - 1), p), pow(y, pow((q + 1) // 4, t + 1, q - 1), q)
	x0 = (q * pow(q, -1, p) * u + p * pow(p, -1, q) * v) % n
	h = []
	for i in range(len(c)):
		h += c[i]
	h = len(h)
	h = int(log2(int(log2(h))))
	#h = 3
	m = []
	for i in range(-1, t - 1):
		x = pow(x0, 2, n)
		x0 = x
		#print(x)
		b = list(map(int, list(bin(x)[2:])))[len(bin(x)) - 2 - h:]
		#print(c[i + 1], b)
		m.append(xor_lists(c[i + 1], b))

	h = []
	for i in range(len(m)):
		h += m[i]
	m = h + c[-1]
	#print(m)
	return m

if __name__ == '__main__':
	p, q = 19, 7
	n = p * q
	m = 123456789
	#m = 41
	if (p % 4 == 3 and q % 4 == 3):
		print(m)
		c = blume_goldwasser_e(n, m)
		print(c)
		mn = blume_goldwasser_d(p, q, c)
		print(int("".join(list(map(str, mn))), 2))
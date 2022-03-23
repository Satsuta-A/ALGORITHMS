from sympy import *
import math as m
from random import randint
def DH(p):
	g = primitive_root(p)
	a , b = randint(2, phi(p) - 1), randint(2, phi(p) - 1)
	#a = 23487261879636
	#b = 12345678987643
	X_a, X_b = pow(g, a, p), pow(g, b, p)
	K_a, K_b = pow(X_b, a, p), pow(X_a, b, p)
	print(f'p = {p}, g = {g}, a = {a}, b = {b}\nX_a = {X_a}, X_b = {X_b}\nK_a = {K_a}, K_b = {K_b}')
	if K_a == K_b:
		return K_a
	else:
		print('Пацан к успеху шёл, не повезло, не фортануло...')

if __name__ == '__main__':
	phi = totient
	#lambd = reduced_totient
	#multiplicative_order = n_order
	p = nextprime(10**15+1000*12)
	print(DH(p))
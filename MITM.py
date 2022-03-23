from sympy import *
from random import randint
def MITM(p):
	g = primitive_root(p)
	a , b = randint(2, p - 1), randint(2, p - 1)
	e = randint(2, p - 1)
	X_a, X_b = pow(g, a, p), pow(g, b, p)
	X_e = pow(g, e, p)
	K_ae, K_be = pow(X_a, e, p), pow(X_b, e, p)
	K_a, K_b = pow(X_e, a, p), pow(X_e, b, p) #K_ae, K_ab
	print(f'p = {p}, g = {g}, a = {a}, b = {b}\nX_a = {X_a}, X_b = {X_b}\nX_e = {X_e}\nK_a = {K_a}, K_b = {K_b}\nK_ae = {K_ae}, K_be = {K_be}')
	if K_ae == K_a and K_be == K_b:
		return K_ae, K_be
	else:
		print('Пацан к успеху шёл, не повезло, не фортануло...')

if __name__ == '__main__':
	#phi = totient
	#lambd = reduced_totient
	#multiplicative_order = n_order
	p = nextprime(10**15+1000*12)
	print(MITM(p))
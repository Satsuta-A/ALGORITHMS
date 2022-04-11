from numpy import poly1d, array, polyder, eye
from numpy import *
from sympy import mod_inverse
from sympy.polys.domains import ZZ
from sympy.polys.galoistools import gf_gcdex, gf_div, gf_pow, gf_factor

def solving(Q: list, p : int, k: int):
	Q.pop(0)
	for x in Q:
		x.pop(0)
	n = len(Q)
	m = len(Q)
	for i in range(n - 1):
		try:
			for j in range(m):
					Q[i][j] = (Q[i][j] * mod_inverse(Q[i][i], p)) % p
			for j in range(i + 1, n):
				if Q[j][i] == 0: 
					continue
				for t in range(m):
					Q[j][t] = (Q[j][t] - Q[i][t]) % p
		except:
			continue

	for x in Q:
		if x == [0]*m:
			Q.pop(Q.index(x))
	"""print('------')
				for x in Q:
					print(x)
				print('------')"""

	h = []
	for i in range(1, k):
		h.append([0] + Q[-k])
		h[i - 1].reverse()
	return h

def conv(lst: list):
	dct = {}
	for x in lst:
		if not tuple(x) in dct.keys():
			dct[tuple(x)] = 1
		else:
			dct[tuple(x)] += 1
	
	return dct

def SF(f: list, p: int):
	if len(f) < 3:
		return [f]
	g = [x % p for x in list(polyder(poly1d(f), m=1))]
	if g == [0]*len(g):
		hp = gf_factor(f, p, ZZ)
		return [hp[1][0][0]] * hp[1][0][1]
	d = gf_gcdex(ZZ.map(f), ZZ.map(g), p, ZZ)
	if d[2] == [1]:
		return [f]
	else:
		h = gf_div(f, d[2], p, ZZ)
		res = SF(d[2], p) + [h[0]]
		return res

def barl(f: list, p: int):
	Q = []
	F = [f]
	for i in range(len(f) - 1):
		x = gf_div(list(poly1d([1, 0]) ** (i * p)), f, p, ZZ)[1]
		x.reverse()
		Q.append(x + [0] * (len(f) - len(x) - 1))
	for i in range(len(f) - 1):
		Q[i][i] = (Q[i][i] - 1) % p
	Q1 = array(Q)
	r = linalg.matrix_rank(Q1)
	k = len(f) - r - 1
	h = [1] + solving(Q, p, k)
	print(h)
	for i in range(1, k):
		for x in F:
			if len(x) > 2:
				F.pop(F.index(x))
				for a in range(p):
					t = h[i]
					t[-1] = (t[-1] - a) % p
					d = gf_gcdex(x, t, p, ZZ)[2]
					print(x, t, gf_gcdex(x, t, p, ZZ))
					F.append(d)
	return F

if __name__ == "__main__":
	print(conv(SF([1, 1, 1, 1, 0, 1, 0, 1], 2)))
	print(conv(SF([1, 0, 5, 4, 2, 4], 7)))
	
	print(gf_factor([1, 1, 1, 1, 0, 1, 0, 1], 2, ZZ))
	print(gf_factor([1, 0, 5, 4, 2, 4], 7, ZZ))

	print(barl([1, 0, 1, 0, 1, 1], 2))
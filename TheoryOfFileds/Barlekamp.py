from numpy import poly1d, array, polyder, eye
from numpy import *
from sympy import mod_inverse
from sympy.polys.domains import ZZ
from sympy.polys.galoistools import gf_gcdex, gf_div, gf_pow, gf_factor

def Gauss(A, p):
    Q1 = array(A)
    r = linalg.matrix_rank(Q1)
    k = len(A) - r - 1
    for i in range(len(A)):
        if A[i][i] == 0:
            continue
        A[i] = list(array(A[i]) * mod_inverse(A[i][i], p) % p)
    for x in A:
        print(x)
    for i in range(len(A) - 1):
        for j in range(i+1, len(A)):
            if A[i][i] == 0:
                continue
            A[j] = list((array(A[j]) - array(A[i]) * A[j][i]) % p)
    print('---------')
    for x in A:
        print(x)
    h = [[1]]
    print(k)
    c = 1
    for i in range(len(A)):
        hp = A[len(A) - i - 1]
        if hp != [0] * len(A):
            h.append(hp)
            c += 1
        if c == k:
            break
    return h, k

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
	h, k = Gauss(Q, p)
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
	#print(conv(SF([1, 1, 1, 1, 0, 1, 0, 1], 2)))
	#print(conv(SF([1, 0, 5, 4, 2, 4], 7)))
	
	#print(gf_factor([1, 1, 1, 1, 0, 1, 0, 1], 2, ZZ))
	#print(gf_factor([1, 0, 5, 4, 2, 4], 7, ZZ))

	print(barl([1, 0, 1, 0, 1, 1], 2))
from sympy import *
from numpy import array, linalg
def Gauss(A, p):
    Q1 = array(Q)
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
    return h

if __name__ == "__main__":
    A =[[2, 3, 4, 5],
        [0, 6, 1, 3],
        [1, 0, 2, 4],
        [5, 2, 0, 2]]
    p = 7
    A = [
        [1, 1, 0, 0],
        [0, 1, 0, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]]
    p = 2
    print(Gauss(A, p))
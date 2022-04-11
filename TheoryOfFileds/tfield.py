from numpy import poly1d, array
from sympy import mod_inverse
import sympy as sp
from sympy.polys.domains import ZZ
from sympy.polys.galoistools import gf_factor

class TF:
    def __init__(self, mod: int, nepr: list, polinom: list):
        if not (gf_factor(ZZ.map(nepr), mod, ZZ)[1][0][1] == 1 and len(gf_factor(ZZ.map(nepr), mod, ZZ)[1]) == 1):
            raise Exception('Nepr error')
        elif sp.isprime(mod) == False:
            raise Exception('Mod error')
        else:
            self.mod = mod
            self.nepr = nepr
            self.repr = list(poly1d(array(-poly1d(self.nepr[1:])) % self.mod))
            
            if len(self.nepr) == len(polinom):
                self.polinom = list(poly1d(polinom[1:]) + polinom[0] * poly1d(self.repr))
                self.polinom = list(poly1d(array(self.polinom) % self.mod))
            elif len(self.nepr) < len(polinom):
                raise Exception('bullshit item')
            else:

                self.polinom = list(poly1d(array(polinom) % self.mod))
            self.size = pow(self.mod, len(self.nepr) - 1) - 1

    def degree(self):
        try:
            return self.all_items_lst.index(self.polinom)
        except:
            self.all()
            return self.all_items_lst.index(self.polinom)
    def all(self, printing=False):
        help_list = TF(self.mod, self.nepr, [1, 0])
        counter = 1
        all_list = [help_list]
        while help_list.polinom != [1]:
            help_list = TF(self.mod, self.nepr, list(poly1d(help_list.polinom) * poly1d([1, 0])))
            counter += 1
            all_list.append(help_list)
        all_list.insert(0, all_list[-1])
        all_list.pop()
        self.all_items = all_list[:]
        self.all_items_lst = [x.polinom for x in self.all_items]
        if printing:
            for i in range(len(all_list)):
                print(i, ':', all_list[i])
        else:
            return all_list
    def __len__(self):
        return len(self.polinom)
    def __str__(self):
        return str(self.polinom)
    def __repr__(self):
        return str(self.polinom)
    def __getitem__(self, i):
        return self.polinom[len(self) - i - 1]
    def __setitem__(self, key, value):
        self.polinom[len(self.polinom) - key - 1] = int(value) % self.mod
    def __add__(self, elem):
        if isinstance(elem, int):
            res = self.polinom[:]
            res[-1] = (elem + res[-1]) % self.mod
            return TF(self.mod, self.nepr, res)
        elif isinstance(elem, TF):
            if self.mod != elem.mod:
                raise Exception('mod elem?')
            elif self.nepr != elem.nepr:
                raise Exception('nepr elem?')
        else:
            raise Exception('type elem?')
        return TF(self.mod, self.nepr, list(poly1d(self.polinom) + poly1d(elem.polinom)))

    def __radd__(self, elem):
        return self+elem

    def __neg__(self):
        return TF(self.mod, self.nepr, list(-poly1d(self.polinom)))
    def __sub__(self, elem):
        if isinstance(elem, int):
            elem = TF(self.mod, nepr, [elem % self.mod])
        elif isinstance(elem, TF):
            if self.mod != elem.mod:
                raise Exception('mod elem?')
            elif self.nepr != elem.nepr:
                raise Exception('nepr elem?')
        else:
            raise Exception('type elem?')
        return TF(self.mod, self.nepr, list(poly1d(self.polinom) - poly1d(elem.polinom)))

    def __mul__(self, elem):
        if isinstance(elem, int):
            res = [(x * elem) % self.mod for x in self.polinom]
            return TF(self.mod, self.nepr, res)
        elif isinstance(elem, TF):
            if self.mod != elem.mod:
                raise Exception('mod elem?')
            elif self.nepr != elem.nepr:
                raise Exception('nepr elem?')
        else:
            raise Exception('type elem?')
        try:
            return TF(self.mod, self.nepr, self.all_items_lst[(self.degree() + elem.degree()) % self.size])
        except:
            self.all()
            return TF(self.mod, self.nepr, self.all_items_lst[(self.degree() + elem.degree()) % self.size])
    
    def __rmul__(self, elem):
        return self * elem

    def __truediv__(self, elem):
        if isinstance(elem, TF):
            if self.mod != elem.mod:
                raise Exception('mod elem?')
            elif self.nepr != elem.nepr:
                raise Exception('nepr elem?')
            else:
                return self * inverse(elem)
        elif isinstance(elem, int):
            return self * mod_inverse(elem, self.mod)
        else:
            print("unsupported types!")

    def inverse(self):
        try:
            print(self.size)
            print(abs(self.degree() - self.size))
            return self.all_items[(abs(self.degree() - self.size) ) % self.size]
        except:
            self.all()
            return self.all_items[(abs(self.degree() - self.size)) % self.size]
    def __pow__(self, power, modulo=None):
        try:
            return self.all_items[self.degree() * power % self.size]
        except:
            self.all()
            return self.all_items[self.degree() * power % self.size]

    def trace(self):
        tr = TF(self.mod, self.nepr, [0])
        if self.polinom == [0]:
            return 0
        for i in range(len(self.nepr) - 1):
            x = pow(self, pow(self.mod, i, self.size))
            tr = tr + x
        return tr[0]
    def minpol(self):
        if self.polinom == [1, 0]:
            n = self.size - 1
        else:
            n = (self.size - 1) // gcd(self.size - 1, self.degree())
        d = n_order(self.mod, n)
        from sympy.abc import y
        for i in range(d):
            break

class pol_for_min():
    def __init__(self, args: list):
        self.coeffs = args[:]

    def __add__(self, val):
        res = []
        a, b = self.coeffs[:], val.coeffs[:]
        a.reverse()
        b.reverse()
        for i in range(len(a)):
            try:
                res.append(a[i] + b[i])
            except:
                res.append(a[i])
        res.reverse()
        return pol_for_min(res)

    def __call__(self, val):
        res = 0
        pwr = 1
        for co in self.coeffs:
            res += co*pwr
            pwr *= val
        return res

    def __mul__(self, val):
        _s = self.coeffs[:]
        _v = val.coeffs[:]
        _s.reverse()
        _v.reverse()
        res = [0]*(len(_s)+len(_v)-1)
        for selfpow,selfco in enumerate(_s):
            for valpow,valco in enumerate(_v):
                res[selfpow+valpow] = res[selfpow+valpow] + selfco*valco
        res.reverse()
        return pol_for_min(res)

    def __neg__(self):
        return self.__class__([-co for co in self.coeffs])

    def _radd__(self, val):
        return self+val

    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__, self.coeffs)

    def __rmul__(self, val):
        return self*val

    def __rsub__(self, val):
        return -self + val

    def __str__(self):
        res = []
        lst = self.coeffs[:]
        lst.reverse()
        for po,co in enumerate(lst):
            if co:
                if po==0:
                    po = ''
                elif po==1:
                    po = 'X'
                else:
                    po = 'X^'+str(po)
                try:
                    res.append(str(co.polinom[-1])+po)
                except:
                    res.append(str(co)+po)
        if res:
            res.reverse()
            return ' + '.join(res)
        else:
            return "0"

    def __sub__(self, val):
        return self.__add__(-val)

if __name__ == "__main__":
    """g1 = TF(3, [1, 2, 1, 1], [1, 2])
                g2 = TF(3, [1, 2, 1, 1], [1, 0, 2])
                g = TF(3, [1, 2, 1, 1], [1, 2, 2])
                print('g', g)
                g.all(True)
                al = g.all()
                print('deg g', g.degree()) 
                print('obr g', g.inverse())
                print('g * g2', g * g2)
                print('deg 1',TF(3, [1, 2, 1, 1], [1]).degree())
                print('obr 1', TF(3, [1, 2, 1, 1], [1]).inverse())
                print(pow(TF(3, [1, 2, 1, 1], [2, 1, 2]), 9))
                print(pow(TF(3, [1, 2, 1, 1], [2]), 2))
                h0, h1, h2 = 1,0,0
                for x in al:
                    tr = x.trace()
                    print(x, ':', tr)
                    if tr == 0:
                        h0 += 1
                    if tr == 1:
                        h1 += 1
                    if tr == 2:
                        h2 += 1
                print(h0, h1, h2)"""

    a = pol_for_min([1, 0, 1, 1, 1])
    b = pol_for_min([1, 1, 1])
    print(a + b)
    x = TF(2, [1, 0, 1, 1], [1, 1])
    y = TF(2, [1, 0, 1, 1], [1, 0, 1])
    z = TF(2, [1, 0, 1, 1], [1, 1, 1])
    a = pol_for_min([1, -x])
    b = pol_for_min([1, -y])
    c = pol_for_min([1, -z])
    print((-x)*(-y))
    print((-x)*(-y)*(-z))
    x.all(True)
    print(x*y)
    print(x*y*z)
    print(a * b)
    print(a * b * c)
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
            elem = TF(self.mod, nepr, [elem % self.mod])
        elif isinstance(elem, TF):
            if self.mod != elem.mod:
                raise Exception('mod elem?')
            elif self.nepr != elem.nepr:
                raise Exception('nepr elem?')
        else:
            raise Exception('type elem?')
        return TF(self.mod, self.nepr, list(poly1d(self.polinom) + poly1d(elem.polinom)))

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
            elem = TF(self.mod, nepr, [elem % self.mod])
        elif isinstance(elem, TF):
            if self.mod != elem.mod:
                raise Exception('mod elem?')
            elif self.nepr != elem.nepr:
                raise Exception('nepr elem?')
        else:
            raise Exception('type elem?')
        #return TF(self.mod, self.nepr, list(poly1d(self.polinom) * poly1d(elem.polinom)))
        return TF(self.mod, self.nepr, self.all_items_lst[(self.degree() + elem.degree()) % 26])
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

if __name__ == "__main__":
    g1 = TF(3, [1, 2, 1, 1], [1, 2])
    g2 = TF(3, [1, 2, 1, 1], [1, 0, 2])
    g = TF(3, [1, 2, 1, 1], [1, 2, 2])
    print('g', g)
    g.all(True)
    print('deg g', g.degree())
    print('obr g', g.inverse())
    print('g * g2', g * g2)
    print('deg 1',TF(3, [1, 2, 1, 1], [1]).degree())
    print('obr 1', TF(3, [1, 2, 1, 1], [1]).inverse())
    print(pow(TF(3, [1, 2, 1, 1], [2, 1, 2]), 9))
    print(pow(TF(3, [1, 2, 1, 1], [2]), 2))
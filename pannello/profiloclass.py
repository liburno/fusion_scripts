import os
from .utils import *

class Profilo:
    def __init__(self, tipo, l , peso=0):
        self.tipo = tipo
        self.l = l
        self.peso = peso

    def __str__(self):
        return self.name()

    def name(self):
        n = self.tipo+" "+str(self.l)+"mm "
        return n


def loadprofili():
    filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "res/lista.txt")
    f = open(filename, "r")
    profili = {}
    for x in f:
        x1 = x+',,,,'
        a = x1.strip().split(',')
        q = toint(a[1])
        if q:
            p = Profilo(a[0].strip(), q)
            profili[p.name()] = p
    return profili


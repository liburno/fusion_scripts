import os
from .utils import *

class PosManiglia:
    def __init__(self,des, distx,disty,lung,posx,posy,orient):
        self.des=des
        self.distx=des
        self.disty=des
        self.lung=des
        self.posx=des
        self.posy=des
        self.orient=des

    def __str__(self):
        return self.des



def loadposman():
    filename = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "res/posman.txt")
    f = open(filename, "r")
    posman = {}
    for x in f:
        x1 = x+',,,,,,,,'
        x1=x1.lower()
        a = x1.strip().split(',')
        q = toint(a[1])
        if a:
            p = PosManiglia(a[0].strip(), q, toint(a[2]), toint(a[3]),a[4].strip(),a[5].strip(),a[6].strip())
            posman[p.des] = p
    return posman


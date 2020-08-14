import os
from .utils import *

class Profilo:
    def __init__ (self,tipo,l,a=0,sp=0,peso=0): 
        self.tipo=tipo
        self.l=l
        if a==0:
           a=l
        self.a=a
        self.sp=sp
        if self.tipo=='r' or self.tipo=='s' or self.tipo=='q' or self.tipo=='' :
            if self.sp:
                self.tipo='s'
            elif self.l==self.a:
                self.tipo='q'
            else:
                self.tipo='r'
       
        self.peso=peso
    def __str__(self):
       return self.name()
    def name(self):
       n=self.tipo+str(self.l)
       if self.a != self.l:
          n=n+str(self.a)
       if self.sp:
          n=n+"x"+str(self.sp)
       return n


def loadprofili():
    filename=os.path.join(os.path.dirname(os.path.realpath(__file__)),"res/lista.txt")
    f = open(filename, "r")
    profili={}
    for x in f:
        x1=x+',,,,'
        a=x1.strip().split(',')
        q=toint(a[1])
        if q:
            p=Profilo(a[0].strip(),q,toint(a[2]),toint(a[3]))
            profili[p.name()]=p
    return profili

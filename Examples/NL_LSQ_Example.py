# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 14:40:55 2013

@author: OMedvedev
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

infile = open('data/temperatures.dat','r')
t=np.genfromtxt(infile,names=True,skip_header=17,skip_footer=2)
tx=t['YEAR']
ty=t['JUN']

def func(coef,X):
    return coef[0]*X*X+coef[1]*X+coef[2]

def residuals(coef,X,Y):
    return Y - func(coef,X)

N=1000
coef0=[1,0.5,1]
X = np.linspace(0,20,N)
Y = func(coef0,X)+(np.random.random(N)-0.5)*0.1

coef,cov,infodict,mesg,ier = opt.leastsq(residuals,coef0,args=(tx,ty),full_output=True)

print(coef)

plt.plot(tx,ty,'o',
         tx, func(coef,tx),'b')
plt.show
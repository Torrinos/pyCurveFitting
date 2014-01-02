# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 14:40:55 2013

@author: OMedvedev
"""

import numpy as np
import matplotlib.pyplot as plt

infile = open('data/temperatures.dat','r')
t=np.genfromtxt(infile,names=True,skip_header=17,skip_footer=2)
tx=t['YEAR']
ty=t['JUN']

split = 0.7

tx1 = tx[0:int(len(tx)*split)]
tx2 = tx[int(len(tx)*split):]

ty1 = ty[0:int(len(ty)*split)]
ty2 = ty[int(len(ty)*split):]

A1 = np.vstack([tx1,np.ones(len(tx1))]).T
a1,b1 = np.linalg.lstsq(A1,ty1)[0]

A2 = np.vstack([tx2,np.ones(len(tx2))]).T
a2,b2 = np.linalg.lstsq(A2,ty2)[0]


plt.plot(tx,ty,'o',
     tx1, a1*tx1+b1,'b',
     tx2, a2*tx2+b2,'r')
plt.show
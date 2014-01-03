# -*- coding: utf-8 -*-
"""
Created on Thu Jan 02 11:43:01 2014

@author: OMedvedev
"""

from ParsingClass import *
from FittingClass import *
from operator import itemgetter

#initiate a parser class
Parser=CParsing()

#Synthetic dataset
tx = np.linspace(0, 10)
#ty = (5. + 0.2*np.sin(2 * tx - 0.1) + \
#    0.1*np.random.normal(size=len(tx), scale=0.3))
ty = 0.1*sqrt(0.2*tx**3)


#read and create function to be used
with open('../Data/ShortList.dat','r') as funcfile:
    myRes = []
    goofits = 0
    totfits = 0
    for line in funcfile:
        totfits += 1        
        try:
            Fitter = CFitting(Parser,line.rstrip(),tx,ty)
            Res=Fitter.Minimize()
            goofits += 1
        except:
            Res=CFitReport(line,None,None,None,None)        
            pass
        #modify this line if you want sorting based on R2 or Chi2        
        myRes.append([Res.R2,Res])
    print ("Good = %d out of %d" %(goofits, totfits) +"\n")
        

#sort results - smallest will be first in the list
#if using R2 need reverse=True
#if using RedChi2 need reverse=False, although too smal RedChi2 may indicate overfitting
myRes.sort(key=itemgetter(0),reverse=True)
#print myRes

with open('../Data/Result.dat','w') as resfile:
    for i in range(3):
        resfile.write("Result %i" %i + "\n")
        resfile.write(myRes[i][1].Report)
        resfile.write("\n")

#try to plot best three results
try:
    import matplotlib.pyplot as plt
    import matplotlib as mpl                                
    colors = ('b','g','r','c','m','y','k','w',)
    mpl.rcParams.update({'font.size': 6})
    plt.plot(tx, ty, 'k+')
    for i in range(3):
        mylabel=myRes[i][1].Function + " -> R2= %.4f" % myRes[i][0]
        plt.plot(tx, ty+myRes[i][1].Result.residual,colors[i],\
            label=mylabel)
        plt.legend()
        plt.show()
except:
    pass
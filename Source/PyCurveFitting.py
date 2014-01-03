# -*- coding: utf-8 -*-
"""
Created on Thu Jan 02 11:43:01 2014

@author: OMedvedev
"""

import MyParser as mp
import lmfit as lm
import numpy as np
#numpy globals are required for StringFunction to work with arrays
from numpy import sin, cos, exp, tan, log
from scitools.StringFunction import StringFunction
from operator import itemgetter

def BasicStats(yvector):
    ave=np.mean(yvector)
    res = 0
    for i in yvector:
        res += (i-ave)**2
    return res

#read data to be fitted
with open('../Data/Temperatures.dat','r') as datafile:
    tt=np.genfromtxt(datafile,names=True,skip_header=17,skip_footer=2)
    tx=tt['YEAR']
    ty=tt['JUN']

#Synthetic dataset
tx = np.linspace(0, 10)
ty = (5. + 0.2*np.sin(2 * tx - 0.1) + \
    np.random.normal(size=len(tx), scale=0.3))
SStot=BasicStats(ty)
    
class CReport:
    def __init__(self,String,Quality,FitResult,FitReport):
        self.Quality = Quality
        self.String = String
        self.Result = FitResult
        self.Report = FitReport

def Fitter(FString):
    result=None
    report=None
    
    myVars=mp.getVars(FString)
    myFunc=StringFunction(FString,independent_variables=myVars,\
        globals=globals())
    
    # create a set of Parameters
    #initial values are defined here
    params = lm.Parameters()
    for i in range(len(myVars)-1):
        params.add(myVars[i],value=1)
      
    # define objective function: returns the array to be minimized
    def ObjFunc(params, x, data):
        myParams = np.zeros(len(params))
        for i in range(len(params)):
            myParams[i]=params[myVars[i]].value
        model = myFunc(*myParams,x=x)
        return model - data
    
    myfit = lm.Minimizer(ObjFunc, params, args=(tx,ty), fcn_kws={})
    myfit.prepare_fit()
    
    result = lm.minimize(ObjFunc, params, args=(tx,ty),method='leastsq')
    report = lm.fit_report(params)
    #quality = result.redchi
    quality = 1-result.chisqr/SStot
    return CReport(FString,quality,result,report)

#read and create function to be used
with open('../Data/ShortList.dat','r') as funcfile:
    myRes = [] 
    for line in funcfile:
        try:
            Res=Fitter(line.rstrip())
        except:
            Res=CReport(line,None,None,None)            
            pass
        myRes.append([Res.Quality,Res])
        

#sort results - smallest will be first in the list
#if using R2 need reverse=True
#if using Chi2 need reverse=False
myRes.sort(key=itemgetter(0),reverse=True)
print myRes

#try to plot best three results
try:
    import matplotlib.pyplot as plt
    colors = ('b','g','r','c','m','y','k','w',)
    matplotlib.rcParams.update({'font.size': 6})
    plt.plot(tx, ty, 'k+')
    for i in range(3):
        mylabel=myRes[i][1].String + " -> R2= %.4f" % myRes[i][0]
        plt.plot(tx, ty+myRes[i][1].Result.residual,colors[i],\
            label=mylabel)
        plt.legend()
        plt.show()
except:
    pass

#with open('../Data/debug','w') as outfile:
#    np.savetxt(outfile, tx)
#    outfile.write(myRes[0][1].String)    
#    np.savetxt(outfile, ty)
#    outfile.write(str(myRes[0][0]))
#    np.savetxt(outfile,ty+myRes[i][1].Result.residual)    
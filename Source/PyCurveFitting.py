# -*- coding: utf-8 -*-
"""
Created on Thu Jan 02 11:43:01 2014

@author: OMedvedev
"""

from MyParser import *
import lmfit as lm
import numpy as np
#numpy globals are required for StringFunction to work with arrays
from numpy import sin, cos, exp, tan, log, sqrt
from scitools.StringFunction import StringFunction
from operator import itemgetter

#initiate a parser class
myParser=EQParser()

def BasicStats(yvector):
    ave=np.mean(yvector)
    res = 0
    for i in yvector:
        res += (i-ave)**2
    return res

"""
#read data to be fitted
with open('../Data/Temperatures.dat','r') as datafile:
    tt=np.genfromtxt(datafile,names=True,skip_header=17,skip_footer=2)
    tx=tt['YEAR']
    ty=tt['JUN']
"""

#Synthetic dataset
tx = np.linspace(0, 10)
#ty = (5. + 0.2*np.sin(2 * tx - 0.1) + \
#    0.1*np.random.normal(size=len(tx), scale=0.3))
ty = 0.1*sqrt(0.2*tx**3)
SStot=BasicStats(ty)
    
class CReport:
    def __init__(self,Function,R2,Chi2,FitResult,FitReport):
        self.R2 = R2
        self.Chi2 = Chi2
        self.Function = Function
        self.Result = FitResult
        self.Report = FitReport

def Fitter(FString):
    result=None
    report=None
    
    try:    
        myVars=myParser.getVars(FString)
    except:
        print ("Can't parse equation %s" %FString +"\n")
        pass
    
    myFunc=StringFunction(FString,independent_variables=myVars,\
        globals=globals())
    
    # create a set of Parameters
    #initial values are defined here
    params = lm.Parameters()
    for i in range(len(myVars)-1):
        params.add(myVars[i],value=0.1)
      
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
    
    #Calculate both quality factors - R2 and ReducedChi2.
    R2 = 1-result.chisqr/SStot
    RChi2 = result.redchi
    return CReport(FString,R2,RChi2,result,report)

#read and create function to be used
with open('../Data/ShortList.dat','r') as funcfile:
    myRes = [] 
    for line in funcfile:
        try:
            Res=Fitter(line.rstrip())
        except:
            Res=CReport(line,None,None,None,None)        
            pass
        #modify this line if you want sorting based on R2 or Chi2        
        myRes.append([Res.R2,Res])
        

#sort results - smallest will be first in the list
#if using R2 need reverse=True
#if using RedChi2 need reverse=False, although too smal RedChi2 may indicate overfitting
myRes.sort(key=itemgetter(0),reverse=True)

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
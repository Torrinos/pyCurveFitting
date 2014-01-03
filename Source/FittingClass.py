# -*- coding: utf-8 -*-
"""
Enclosure for the fitting class
Instance will return LMFIT Minimizer object for given function string
Created on Fri Jan 03 11:54:58 2014

@author: OMedvedev
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 02 11:43:01 2014

@author: OMedvedev
"""
import lmfit as lm
import numpy as np
from ParsingClass import *
from numpy import sin, cos, exp, tan, log, sqrt
from scitools.StringFunction import StringFunction

class CFitReport():

    def __init__(self,Function,R2,Chi2,FitResult,FitReport):
        self.R2 = R2
        self.Chi2 = Chi2
        self.Function = Function
        self.Result = FitResult
        self.Report = FitReport

class CFitting():

    def __init__(self,Parser,fstring,xval,yval):
        self._Function = fstring
        self._Parser = Parser #use existing parser
        self._Variables = self._getVariables()
        self._StringFunction = self._getStringFunction()
        self._Xvalues = xval
        self._Yvalues = yval
        
    def _getVariables(self):
        try:    
            return self._Parser.getVars(self._Function)
        except:
            print ("Can't parse equation %s" %self._Function +"\n")
            pass
             
    def _getStringFunction(self):
        #Create function out of string
        try:        
            return StringFunction(self._Function, \
                independent_variables=self._Variables, \
                globals=globals())
        except:
            print ("Can't create function %s" %self._Function + "\n")

    #calculate SS total for R2 calculation    
    def _getSStotal(self,yvalues):
        ave=np.mean(yvalues)
        res = 0
        for i in yvalues:
            res += (i-ave)**2
        return res
        
    # define objective function: returns the array to be minimized
    def _ObjFunc(self,params, x, data):
        myParams = np.zeros(len(params))
        for i in range(len(params)):
            myParams[i]=params[self._Variables[i]].value
        model = self._StringFunction(*myParams,x=x)
        return model - data


    def Minimize(self):
        result=None
        report=None

        # create a set of Parameters, except x
        #initial values are defined here
        params = lm.Parameters()
        for i in range(len(self._Variables)-1):
            params.add(self._Variables[i],value=0.1)
        
        myfit = lm.Minimizer(self._ObjFunc, params, \
            args=(self._Xvalues, self._Yvalues), \
            fcn_kws={})
        myfit.prepare_fit()
        
        result = lm.minimize(self._ObjFunc, params, \
            args=(self._Xvalues,self._Yvalues), \
            method='leastsq')
        report = lm.fit_report(params)
        
        #Calculate both quality factors - R2 and ReducedChi2.
        R2 = 1-result.chisqr/self._getSStotal(self._Yvalues)
        RChi2 = result.redchi
        return CFitReport(self._Function,R2,RChi2,result,report)
# -*- coding: utf-8 -*-
"""
Parser for mathematical expressions written in F(X)=Y form
in inflix notation

Created on Tue Dec 31 11:21:35 2013

@author: OMedvedev
"""

def _parser(expr):
"""
#sympy version - not scalable

    from sympy import symbols, lambdify,var
    #from sympy.abc import x,y,a,b,c,d,e,f,g,h
    a,b,c,d = symbols('a:d',real=True)
    e,f,g,h = symbols('e:h',real=True)
    i,j,k,l = symbols('i:l',real=True)    
    x,y,z = symbols('x:z', real=True)
    
    A,B,C,D = symbols('A:D',real=True)
    E,F,G,H = symbols('E:H',real=True)
    I,J,K,L = symbols('I:L',real=True)    
    X,Y,Z = symbols('x:z', real=True)
    f=lambdify([a,b,c,d,x],expr,'numpy')
    return f
"""

expr='a*x**2+b*sin(x)+c*x+d'
func=_parser(expr)
print func(1,2,3,4,5)
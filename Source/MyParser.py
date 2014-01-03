# -*- coding: utf-8 -*-
"""
Parser for mathematical expressions written in F(X) form

Created on Tue Dec 31 11:21:35 2013

@author: OMedvedev
"""

"""
#sympy version - scalability issues with variables list
#def _parser(expr):
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

import pyparsing as pp
from numpy import *
from scitools.StringFunction import StringFunction

global varStack
varStack = []

def addVar(varString, tokens):
    varStack.append( tokens[0] )

def defPattern():
    pattern = None        
    #defining sub-variables for tokens
    pi    = pp.CaselessLiteral( "$PI" )
    e     = pp.CaselessLiteral( "$E" )
    plus  = pp.Literal( "+" )
    minus = pp.Literal( "-" )
    mult  = pp.Literal( "*" )
    div   = pp.Literal( "/" )
    lpar  = pp.Literal( "(" ).suppress()
    rpar  = pp.Literal( ")" ).suppress()
    point = pp.Literal( "." )

    #defining variables     
    fnumber = pp.Combine( pp.Word( "+-"+pp.nums, pp.nums ) + 
                       pp.Optional( point + pp.Optional( pp.Word( pp.nums ) ) ) +
                       pp.Optional( e + pp.Word( "+-"+pp.nums, pp.nums ) ) )
    #ident = pp.Word(pp.alphas, pp.alphas+pp.nums+"_$")
    funct = pp.oneOf("sin cos tan log exp log",caseless=True)
    varia = pp.Word( pp.srange("[a-zA-Z_]"),max=1)
    addop  = plus | minus
    mulop = mult | div
    expop = pp.Literal( "**" )

    #defining pattern itself
    expr = pp.Forward()
    atom = (pp.Optional("-") + ( pi | e | varia.addParseAction(addVar) | fnumber | funct + lpar + expr + rpar ) | ( lpar + expr.suppress() + rpar )) 
    # by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-righ
    # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
    factor = pp.Forward()
    factor << atom + pp.ZeroOrMore( ( expop + factor ))
    
    term = factor + pp.ZeroOrMore( ( mulop + factor ))
    expr << term + pp.ZeroOrMore( ( addop + term ))
    pattern = expr
    return pattern

def getVars(testString):
    defPattern().parseString(testString)
    return sorted(set(varStack))

def test(myFStr):
    myVars=getVars(myFStr)
    Fun=StringFunction(myFStr,independent_variables=myVars,globals=globals())
    
    x=linspace(0,100)    
    
    Par=zeros(len(myVars)-1)
    for i in range(len(myVars)-2):
        Par[i]=i+0.2
    return (Fun(*Par,x=x),2+4*cos(x)+sin(x))
    #return Par[0]+Par[1]*x**2

#print getVars("a+b*sin(c*x)")
#print test("a+b*x+c*x**2+cos(x)")
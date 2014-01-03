# -*- coding: utf-8 -*-
"""
Parser for mathematical expressions written in F(X) form
Class EQParser is used to par

Created on Tue Dec 31 11:21:35 2013
@author: OMedvedev
"""

class CParsing():
    def __init__(self):
        self._varStack = []
        self._pattern = self._defPattern()
    
    def _defPattern(self):
        import pyparsing as pp
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
        funct = pp.oneOf("sin cos tan log exp log sqrt",caseless=True)
        varia = pp.Word( pp.srange("[a-zA-Z_]"),max=1)
        addop  = plus | minus
        mulop = mult | div
        expop = pp.Literal( "**" )
    
        #defining pattern itself
        expr = pp.Forward()
        atom = (pp.Optional("-") + ( pi | e | varia.addParseAction(self._addVar2Stack) | 
            fnumber | funct + lpar + expr + rpar ) | ( lpar + expr.suppress() + rpar )) 
        # by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", 
        # we get right-to-left exponents, instead of left-to-righ
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = pp.Forward()
        factor << atom + pp.ZeroOrMore( ( expop + factor ))
        
        term = factor + pp.ZeroOrMore( ( mulop + factor ))
        expr << term + pp.ZeroOrMore( ( addop + term ))
        pattern = expr
        return pattern
        
    def _addVar2Stack(self,varString,tokens):
        self._varStack.append( tokens[0])
        
    def getVars(self,testString):
        self._pattern.parseString(testString)
        return sorted(set(self._varStack))
        
#Test Section, please ignore
if __name__ == "__main__":
    from numpy import *
    from scitools.StringFunction import StringFunction

    def test(myFStr,Params,X):

        myEQParser = EQParser()
        myVars=myEQParser.getVars(myFStr)
        Fun=StringFunction(myFStr,independent_variables=myVars,globals=globals())
        return Fun(*Params,x=X)
        
    myEQParser = EQParser()

    print test("a+b*cos(c*x)+sin(x)",([2,4,5.1]),1.21)-(2+4*cos(5.1*1.21)+sin(1.21))
    print test("a+b**c**d**x",([1.1,2.1,.12,4.2]),1.298)-(1.1+2.1**0.12**4.2**1.298)
    print test("a*exp((x-b)**2/c)",([0.25,0.2,0.456]),0.987e+0)-(0.25*exp((0.987-0.2)**2/0.456))
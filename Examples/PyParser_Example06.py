# fourFn.py
#
# Demonstration of the pyparsing module, implementing a simple 4-function expression parser,
# with support for scientific notation, and symbols for e and pi.
# Extended to add exponentiation and simple built-in functions.
# Extended test cases, simplified pushFirst method.
#
# Copyright 2003-2006 by Paul McGuire
#
from pyparsing import *

varStack = []

def addVar(varString, tokens):
    varStack.append( tokens[0] )

bnf = None
def BNF():
    """
    expop   :: '^'
    multop  :: '*' | '/'
    addop   :: '+' | '-'
    integer :: ['+' | '-'] '0'..'9'+
    atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
    factor  :: atom [ expop factor ]*
    term    :: factor [ multop factor ]*
    expr    :: term [ addop term ]*
    """
    global bnf
    if not bnf:
        pi    = CaselessLiteral( "PI" )
        e     = CaselessLiteral( "E" )

        point = Literal( "." )
        fnumber = Combine( Word( "+-"+nums, nums ) + 
                           Optional( point + Optional( Word( nums ) ) ) +
                           Optional( e + Word( "+-"+nums, nums ) ) )
        ident = Word(alphas, alphas+nums+"_$")
        funct = oneOf("sin cos tan",caseless=True)
        varia = Word( srange("[a-zA-Z_]"),max=1)
        
        plus  = Literal( "+" )
        minus = Literal( "-" )
        mult  = Literal( "*" )
        div   = Literal( "/" )
        lpar  = Literal( "(" ).suppress()
        rpar  = Literal( ")" ).suppress()
        addop  = plus | minus
        multop = mult | div
        expop = Literal( "^" )

        
        expr = Forward()
        atom = (Optional("-") + ( pi | e | varia.addParseAction(addVar) | fnumber | funct + lpar + expr + rpar ) | ( lpar + expr.suppress() + rpar )) 
        
        # by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-righ
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + ZeroOrMore( ( expop + factor ))
        
        term = factor + ZeroOrMore( ( multop + factor ))
        expr << term + ZeroOrMore( ( addop + term ))
        bnf = expr
    return bnf

print BNF().parseString("a+b*x+sin(x^a)+cos(x/d+l)")
print varStack
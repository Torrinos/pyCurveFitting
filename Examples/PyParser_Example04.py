from pyparsing import *

# define grammar
e = CaselessLiteral('E')
pi = CaselessLiteral('pi')

varlist=[]

def store_vars(tokens):
    var2keep = tokens[0]
    varlist.append(var2keep)

expoop = Literal('^')
signop = oneOf('+ -')
multop = oneOf('* /')
plusop = oneOf('+ -')
factop = Literal('!')

integer = Word(nums)
variable = Word(alphas,exact=1)
operand = variable

funcop = oneOf('cos sin tan')
funcexpr = funcop + '(' + operand + ')'

pattern = operatorPrecedence( operand.setParseAction(store_vars),
    [(factop, 1, opAssoc.LEFT),
     (expoop, 2, opAssoc.RIGHT),
     (signop, 1, opAssoc.RIGHT),
     (multop, 2, opAssoc.LEFT),
     (plusop, 2, opAssoc.LEFT),
     (funcop, 1, opAssoc.RIGHT)]
    )

expr="a+b*x+c*(x+d)+a^x+c!+cos x"

#print pattern.parseString(expr)

result=pattern.parseString(expr)
print result.values
for operand in result:
    print operand.const


print varlist

"""
# map operator symbols to corresponding arithmetic operations
opn = { "+" : ( lambda a,b: a + b ),
        "-" : ( lambda a,b: a - b ),
        "*" : ( lambda a,b: a * b ),
        "/" : ( lambda a,b: a / b ),
        "^" : ( lambda a,b: a ** b ),
         }

# Recursive function that evaluates the stack
def evaluateStack( s ):
  op = s.pop()
  if op in "+-*/^":
    op2 = evaluateStack( s )
    op1 = evaluateStack( s )
    return opn[op]( op1, op2 )
  elif op == "PI":
    return math.pi
  elif op == "E":
    return math.e
  elif re.search('^[a-zA-Z][a-zA-Z0-9_]*$',op):
    if variables.has_key(op):
      return variables[op]
    else:
      return 0
  elif re.search('^[-+]?[0-9]+$',op):
    return long( op )
  else:
    return float( op )

if __name__ == '__main__':
  # input_string
  input_string=''
  
  # Display instructions on how to quit the program
  print "Type in the string to be parse or 'quit' to exit the program"
  input_string = raw_input("> ")
  
  while input_string != 'quit':
    # Start with a blank exprStack and a blank varStack
    exprStack = []
    varStack  = []
  
    if input_string != '':
      # try parsing the input string
      try:
        L=pattern.parseString( input_string )
        print L
      except ParseException,err:
        L=['Parse Failure',input_string]
      
      # show result of parsing the input string
      if debug_flag: print input_string, "->", L
      if len(L)==0 or L[0] != 'Parse Failure':
        if debug_flag: print "exprStack=", exprStack
  
        # calculate result , store a copy in ans , display the result to user
        result=evaluateStack(exprStack)
        variables['ans']=result
        print result
  
        # Assign result to a variable if required
        if debug_flag: print "var=",varStack
        if len(varStack)==1:
          variables[varStack.pop()]=result
        if debug_flag: print "variables=",variables
      else:
        print 'Parse Failure'
        print err.line
        print " "*(err.column-1) + "^"
        print err
  
    # obtain new input string
    input_string = raw_input("> ")
  
  # if user type 'quit' then say goodbye
  print "Good bye!"

"""
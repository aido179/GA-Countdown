#!python3
import math
from gacore.lispeval import ExpressionConstraintError

#Define Grammar non-terminals
class symbols:

    class varConstraint():
        def __init__(self):
            self.varList = [50 , 8 , 3 , 7 , 2 , 10]

        def getVal(self, val):
            if len(self.varList) == 0:
                return "N"
            else:
                pos = val % len(self.varList)
                out = self.varList[pos]
                del self.varList[pos]
                return out

    def __init__(self, startExp):
        con = self.varConstraint()
        self.constraints = {'varConstraint':con}
        self.startExp = startExp

    def callable(self, func):
        try:
            return callable(getattr(self, func))
        except:
            return False

    def call(self, func, sym):
        try:
            return getattr(self, func)(sym)
        except AttributeError:
            return False

    def startExpression(self):
        return self.startExp

    def exp(self,sym):
        sequences = [['op2', 'exp', 'exp'], 'var']
        return self.selectRange(sym,sequences)

    def op2(self,sym):
        sequences = ["add","subtract","multiply","divide"]
        return self.selectRange(sym,sequences)

    def var(self,sym):
        val = self.constraints["varConstraint"].getVal(sym)
        #sequences = [50 , 8 , 3 , 7 , 2 , 10]
        return val
        #return sequences[sym % len(sequences)]

    #replaces modulo based expression selecton with
    #range based selection.
    #Assumes codon range of 0-255.
    def selectRange(self, sym, sequences):
        rangeSize = 256/len(sequences)
        selectedRange = math.floor(sym/rangeSize)
        return sequences[selectedRange]




#Define Grammar terminals (eval'd by evaluator)

def add(n1, n2):
    try:
        return n1+n2
    except TypeError:
        if type(n1) is str:
            return n2
        elif type(n2) is str:
            return n1
        else:
            return "N"

def subtract(n1, n2):
    try:
        out = n1-n2
        if out < 0:
            raise ExpressionConstraintError
        return out
    except TypeError:
        if type(n1) is str:
            return n2
        elif type(n2) is str:
            return n1
        else:
            return "N"

def multiply(n1, n2):
    try:
        return n1*n2
    except TypeError:
        if type(n1) is str:
            return n2
        elif type(n2) is str:
            return n1
        else:
            return "N"

def divide(n1, n2):

    try:
        try:
            out =  n1/n2
            if (out % 1) > 0:
                raise ExpressionConstraintError
            return out
        except TypeError:
            if type(n1) is str:
                return n2
            elif type(n2) is str:
                return n1
            else:
                return "N"
    except ZeroDivisionError:
        return 0


terminals = {'add':add, 'subtract':subtract, 'multiply':multiply, 'divide':divide}

s = symbols("exp")

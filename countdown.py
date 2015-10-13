#!python3

import gacore.grammar as grammar
from countdowngrammar import symbols, terminals
from gacore.lispeval import evaluator, ExpressionConstraintError
from gacore.simplega import population, individual
import math
import winsound
import os
import time


log = "None"

def fitnessFunction(chromo, setPheno = False):
    #build program
    try:
        s1 = symbols("exp")
        g = grammar.builder(s1)
        built = g.buildList(chromo)
        if callable(setPheno):
            setPheno(built)
        #print(built)
    except RecursionError:
        if log == "Error":
            print("Recursion Error, fitness 0")
        return 0

    #execute program
    try:
        lisp = evaluator(terminals)
        evaluated = lisp.eval(*built)
        if type(evaluated) is str:
            evaluated = 0
        #fitness is greater the closer we get to goal
        goal = 556
        return goal - math.fabs(evaluated - goal)
    except OverflowError:
        if log == "Error":
            print("OverFlow Error, fitness 0")
        return 0
    except ExpressionConstraintError:
        if log == "Error":
            print("Constraint Broken.")
        return 0

def results():
    #play noise
    Freq = 2500 # Set Frequency To 2500 Hertz
    Dur = 1000 # Set Duration To 1000 ms == 1 second
    winsound.Beep(Freq,Dur)

    print("|\n|\n|\n|\tRESULTS\n========================")
    p.look()
    print("|\n|\n|\n| BEST:")
    try:
        lisp = evaluator(terminals)
        evaluated = lisp.eval(*p.bestInd.getPheno())
        print (evaluated)
        print(str(p.bestInd.getPheno()))
    except OverflowError:
        print("Overlfow error in evaluator.")

def endCriterea():
    if p.bestInd.getFitness() == 556:
        return True
    elif (len(bestResults) > 100) and ( max(bestResults[-100:]) == min(bestResults[-100:]) ):
        return True
    else:
        return False




p = population(500, 25, fitnessFunction)
i = 0
bestResults = []
fileName = os.path.join('results','countdown',time.strftime("%a %b %d-%H %M")+".csv")
f = open(fileName, 'w')
f.write('Generation,Mutation Rate,Best Fitness,Average Fitness,Plateau Length\n')

while True:
    bestResults.append(p.bestInd.getFitness())

    if endCriterea():
        results()
        break
    #vary mutation rate
    amtBest = bestResults[-100:].count(p.bestInd.getFitness())
    mutation = (1/amtBest) + (amtBest/200)
    #save generation info to file
    popStats = p.stats()
    f.write('{0},{1},{2},{3},{4}\n'.format(i,mutation,popStats['topFitness'],popStats['avgFitness'],amtBest))
    #go to next generation
    p.nextGen(0.8,mutation)
    if i % 10 == 0:
        p.glance()
    print("Gen: "+str(i)+" Mut: "+str(mutation),end="\r")
    i+=1

#free resources
f.close()

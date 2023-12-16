# -*- coding: utf-8 -*-
"""
Created on 22/06/2022

@author: Enzo Venon

This script was made to calculate the probability of getting S successes by throwing D dice in the system from World of Darkness 5th edition (VTM, HTR).

We roll d10. A die has 50 % chance of getting a success or a failure. Until now it's easy.
Now, take into account that a die has 1/10 chance of getting a special success, which, combined with another special success, gets you 4 successes instead of 2.

The following calculations are based on the sum of different ways of getting S successes multiplied by the number of possible permutations that you can find in french here:
https://fr.wikipedia.org/wiki/Combinatoire
Example of calculation: P(S=4, D) = (D!/((D-2)!2!)) * 0.5**(D-2) * 0.1**2 + (D!/((D-4)!4!)) * 0.5**(D-4) * 0.4**4 + (D!/((D-4)!3!1!)) * 0.5**(D-4) * 0.4**3 * 0.1
"""
import matplotlib.pyplot as plt
from math import factorial as fact



def clean(number):
    """Approximates the values of input float in a really weird way.\n
    Parameters
    ----------
    number float: Number to be approximated.
    return float: Number approximated.
    """
    res = str(number)
    if "e" in res:
        if len(res)-4 > 15:
            res = res[0:15] + res[-4:] #I use 15 instead of 16 just in case...
    else:
        if len(res) > 17:
            res = res[0:17]
    res = float(res)
    return res



def list2csv(L):
    """Write a CSV file from a table.\n
    Parameters
    ----------
    L list<list<float>>: Table to be written in a csv.
    """
    text = ""
    for l in range(len(L)):
        for c in range(len(L[l])):
            text+= str(L[l][c]) + ","
        text = text[0:-1] + "\n"
    print(text)
    f = open("proba_V5.csv",'w')
    f.write(text)
    f.close()
    return



def PC(C, S, D):
    """Private. Probability to get S successes with C critical successes by launching D dice.
    Caution: 4*C < S.\n
    Parameters
    ----------
    C int: Natural integer being the number of critical successes expected. C=1 means that we expect to get two 10, so at least 4 successes.
    S int: Natural integer being the total number of successes expected.
    D int: Natural integer being the number of dice thrown.
    return float: Probability to get S successes with C critical successes by launching D dice.
    """
    if 4*C >= S:
        raise Exception("This function returns a wrong result for C >= S/4.")
    PC = 0
    if S <= D + 2*C:
        PC = 1
        for i in range(S - 2*C):
            PC*= (D-i) #Cela devrait s'arrêter à D-(S-2*C-1)
        PC*= (1/(8*C + 4) + 1/(S - 4*C)) * 0.5**(D + 2*C - S) * 0.1**(2*C) * 0.4**(S - 4*C)
        PC/= (fact(2*C)*fact(S - 4*C - 1))
    return PC



def P(S, D, cleanup=True):
    """Probability to get S successes by throwing D dice.\n
    Parameters
    ----------
    S int: Natural integer being the number of successes expected.
    D int: Natural integer being the number of dice thrown.
    cleanup boolean: Removing the floating point error (in a weird way) or not.
    return float: Probability to get S successes by throwing D dice.
    """
    if S < 0 or D < 0:
        raise Exception("S and D must be >=0.")
    else:
        P = 0
        if S > D + D//2 * 2:
            P = 0
        elif S%4!=0:
            for i in range(S//4 + 1):
                P+= PC(i, S, D)
        elif S==0:
            P = 0.5**D
        else:
            for i in range(S//4):
                P+= PC(i, S, D)
            halfPC = 1
            for i in range(S//2):
                halfPC*= (D-i) #This should stop at D-(S/2-1)
            halfPC*= 0.5**(D - S//2) * 0.1**(S//2)
            halfPC/= fact(S//2)
            P+= halfPC
        if cleanup:
            P = clean(P)
        return P



def Plist(D):
    """Generates the list of probabilities of possible outcomes on a D dice throw.
    Parameters
    ----------
    D int: Natural integer being the number of dice thrown.
    return list<float>: Probabilities list on a D dice throw. The index is the number of successes expected.
    """
    Plist = []
    Smax = D//2 *2 + D
    for S in range(Smax + 1):
        Plist.append(P(S, D))
    return Plist



def loopPlist(Dmax):
    res = []
    for D in range(Dmax + 1):
        res.append(Plist(D))
    return res



def show(D):
    y = Plist(D)
    for i in range(len(y)):
        y[i]*=100
    fig, ax = plt.subplots()
    #plt.axhline(y = 5, color = 'grey', linestyle = '--', linewidth=0.75)
    #plt.axhline(y = 10, color = 'grey', linestyle = '--', linewidth=0.75)
    #plt.axhline(y = 15, color = 'grey', linestyle = '--', linewidth=0.75)
    #plt.axhline(y = 20, color = 'grey', linestyle = '--', linewidth=0.75)
    #plt.axhline(y = 25, color = 'grey', linestyle = '--', linewidth=0.75)
    ax.bar([i for i in range(len(y))],y, width=0.96)
    ax.set_ylabel('% chance')
    ax.set_xlabel('Number of successes')
    ax.set_title(str(D) + ' dice')
    ax.set_xticks([i for i in range(len(y))])
    #ax.set_yticks([i*5 for i in range(5)])
    plt.show()
    return



def showCompare(D1, D2):
    y1 = Plist(D1)
    y2 = Plist(D2)
    for i in range(len(y1)):
        y1[i]*=100
    for i in range(len(y2)):
        y2[i]*=100
    fig, ax = plt.subplots()
    ax.bar([i for i in range(len(y1))],y1, alpha=0.75, width=0.96)
    ax.bar([i for i in range(len(y2))],y2, alpha=0.75, width=0.96)
    ax.set_ylabel('% chance')
    ax.set_xlabel('Number of successes')
    ax.set_title(str(D1) + ' and ' + str(D2) + ' dice')
    ax.set_xticks([i for i in range(max(len(y1), len(y2)))])
    plt.show()
    return
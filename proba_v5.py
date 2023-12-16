# -*- coding: utf-8 -*-
"""
Created on Jun 22 2022

@author: Enzo Venon

Ce code a pour but de calculer la probabilité de faire S succès en lançant D dés avec le système de dé du World of Darkness V5 (VtM 5e et HtR 5e).

Un dé à une chance sur deux de rapporter un succès ou de ne pas en rapporter. Jusque là, c'est très simple.
Rajoutons maintenant qu'un dé à une chance sur dix de rapporter un succès spécial, qui, combiné avec un autre succès spécial, donne quatre succès au lieu de deux.

Le principe de la solution repose sur l'addition de différentes façons d'avoir un certains nombre de succès multiplié par le nombre de permutation possible.
https://fr.wikipedia.org/wiki/Combinatoire
Exemple de solution : P(S=4, D) = (D!/((D-2)!2!)) * 0.5**(D-2) * 0.1**2 + (D!/((D-4)!4!)) * 0.5**(D-4) * 0.4**4 + (D!/((D-4)!3!1!)) * 0.5**(D-4) * 0.4**3 * 0.1
"""
import matplotlib.pyplot as plt
from math import factorial as fact



def clean(number):
    """Supprime la légère erreur de calcul des float de python de manière sale.
    Parameters
    ----------
    number float:
    return float:
    """
    res = str(number)
    if "e" in res:
        if len(res)-4 > 15:
            res = res[0:15] + res[-4:] #La vrai limite serait de mettre 16 au lieu de 15, mais dans le doute...
    else:
        if len(res) > 17:
            res = res[0:17]
    res = float(res)
    return res



def list2csv(L):
    """Crée un CSV à partir d'une liste de liste.
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
    """Private. Probabilité, en lançant D dés, de faire S succès avec C succès critiques (C est le nombre de double 10 obtenus).
    Attention : 4*C < S.
    Parameters
    ----------
    C int: Entier naturel correspondant au nombre de succès critiques qu'on s'attend à obtenir. C=1 signifie qu'on s'attend à avoir deux 10, donc au moins 4 succès.
    S int: Entier naturel correspondant au nombre de succès totaux attendus.
    D int: Entier naturel correspondant au nombre de dés lancés.
    return float: Probabilité, en lançant D dés, de faire S succès avec C succès critiques.
    """
    if 4*C >= S:
        raise Exception("Cette fonction donne un résultat incorrect pour C >= S/4.")
    PC = 0
    if S <= D + 2*C:
        PC = 1
        for i in range(S - 2*C):
            PC*= (D-i) #Cela devrait s'arrêter à D-(S-2*C-1)
        PC*= (1/(8*C + 4) + 1/(S - 4*C)) * 0.5**(D + 2*C - S) * 0.1**(2*C) * 0.4**(S - 4*C)
        PC/= (fact(2*C)*fact(S - 4*C - 1))
    return PC



def P(S, D, cleanup=True):
    """Probabilité d'obtenir S succès en lançant D dés.
    Parameters
    ----------
    S int: Entier naturel correspondant au nombre de succès espérés.
    D int: Entier naturel correspondant au nombre de dés lancés.
    cleanup boolean: Enlever la floating point error (de manière sale) ou pas.
    return float: Probabilité d'obtenir S succès en lançant D dés.
    """
    if S < 0 or D < 0:
        raise Exception("S et D doivent être >=0.")
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
                halfPC*= (D-i) #Cela devrait s'arrêter à D-(S/2-1)
            halfPC*= 0.5**(D - S//2) * 0.1**(S//2)
            halfPC/= fact(S//2)
            P+= halfPC
        if cleanup:
            P = clean(P)
        return P



def Plist(D):
    """Génère la liste des probabilités des résultats possibles sur un lancer de D dés.
    Parameters
    ----------
    D int: Entier naturel correspondant au nombre de dés lancés.
    return list<float>: Liste des probabilités sur un lancés de D dés. L'indice est le nombre de succès espérés.
    """
    Plist = []
    Smax = D//2 *2 + D
    for S in range(Smax + 1):
        Plist.append(P(S, D))
    return Plist



def boucleP(Dmax):
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
    ax.set_ylabel('% de chance')
    ax.set_xlabel('Nombre de succès')
    ax.set_title(str(D) + ' dés')
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
    ax.set_ylabel('% de chance')
    ax.set_xlabel('Nombre de succès')
    ax.set_title(str(D1) + ' et ' + str(D2) + 'dés')
    ax.set_xticks([i for i in range(max(len(y1), len(y2)))])
    plt.show()
    return
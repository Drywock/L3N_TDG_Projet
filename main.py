"""
    file : main.py
    author(s) : Thomas LINTANF
    version : 2.0
"""

import logging as log
from graph import Graph

def main():
    """
        Programme principal

        Version : 2.2
    """
    print('Bienvenue !')

    continuer = True

    while(continuer):
        reponse = int(input('Choisissez un graphe entre 1 et 10 (0 pour quitter): '))

        if reponse == 0:
            continuer = False

        elif reponse < 1 or reponse > 10 :
            print("Reponse invalide !")

        else:
            log.basicConfig(format='%(message)s' , level=log.DEBUG)
            fileHandler = log.FileHandler(filename='L3N_B10_trace{0}.txt'.format(reponse), mode='w')
            log.getLogger('').addHandler(fileHandler)

            g = Graph()
            g.readFile('L3N_B10_g{0}.txt'.format(reponse))
            log.info('')
            log.info(g)
            log.info('')
            if not g.detectionCircuit():
                log.info('')
                g.calcRang()
                log.info('')
                if g.estGraphOrdonnancement():
                    log.info('')
                    g.calcCalendPtot()
                    log.info('')
                    g.calcCalendPtard()
                    log.info('')
                    g.calcMarges()
                    log.info('')

            log.getLogger('').removeHandler(fileHandler)

def testGraph():
    """
        Test les differentes methodes de la class Graph

        Version : 2.0
    """
    log.basicConfig(filename='test.txt',format='%(message)s' , level=log.DEBUG)
    g = Graph()
    g.readFile('Graph_0.txt')
    g.calcRang()
    g.detectionCircuit()
    g.calcRang()
    g.calcCalendPtot()
    g.calcCalendPtard()
    g.calcMarges()
    log.info(g)

main()
"""
    file : main.py
    author(s) : Thomas LINTANF
    version : 2.0
"""

import logging as log
from L3NEW_TG_B10_graph import Graph

def main():
    """
        Programme principal

        Version : 2.2
    """
    print('Bienvenue !')

    continuer = True

    while continuer:
        reponse = int(input('Choisissez un graphe entre 1 et 10 (0 pour quitter): '))

        if reponse == 0:
            continuer = False

        elif reponse < 1 or reponse > 10:
            print("Reponse invalide !")

        else:
            log.basicConfig(format='%(message)s', level=log.DEBUG)
            file_handler = log.FileHandler(filename='L3NEW_TG_B10_trace%s.txt' % reponse, mode='w')
            log.getLogger('').addHandler(file_handler)

            graphe = Graph()
            graphe.read_file('L3NEW_TG_B10_g{0}.txt'.format(reponse))
            log.info('')
            log.info(graphe)
            log.info('')
            if not graphe.detection_circuit():
                log.info('')
                graphe.calc_rang()
                log.info('')
                if graphe.est_graph_ordonnancement():
                    log.info('')
                    graphe.calc_calend_plus_tot()
                    log.info('')
                    graphe.calc_calend_plus_tard()
                    log.info('')
                    graphe.calc_marges()
                    log.info('')

            log.getLogger('').removeHandler(file_handler)

def test_graph():
    """
        Test les differentes methodes de la class Graph

        Version : 2.0
    """
    log.basicConfig(filename='test.txt', format='%(message)s', level=log.DEBUG)
    graphe = Graph()
    graphe.read_file('Graph_0.txt')
    graphe.calc_rang()
    graphe.detection_circuit()
    graphe.calc_rang()
    graphe.calc_calend_plus_tot()
    graphe.calc_calend_plus_tard()
    graphe.calc_marges()
    log.info(graphe)

main()

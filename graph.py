"""
    file : graph.py
    author(s) : Thomas LINTANF
    Version : 1.0

    Definition de la classe Graph qui permet de stocker un graph orienter et de lui
    appliquer différent algorithme.
"""

import csv

class Graph :
    """ 
        classe Graph  : représente un graphe orienté 
        
        Version: 1.0
    """

    def __init__(self):
        """ 
            constructeur de la classe Graph

            Version: 1.0
        """

        self.nbSommets = 0
        self.nbArcs = 0
        self.mAdjacence = []
        self.mValeurs = []

    def readFile(self,address):
        """
            Charge un graphe depuis un fichier txt au format csv

            version : 1.0
        """

        with open(address) as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quoting = csv.QUOTE_NONNUMERIC)
            # stockage temporaire des données dans un tableau
            lRows = []
            for row in reader:
                lRows.append(row)

            # extraction du nombre de sommets et d'arcs
            self.nbSommets = int(lRows[0][0])
            self.nbArcs = int(lRows[1][0])

            # Initialisation des matrices d'adjacense et des valeurs
            for si in range(0, self.nbSommets):
                lA = []
                lV = []
                for sJ in range(0, self.nbSommets):
                    lA.append(False)
                    lV.append('*')
                self.mAdjacence.append(lA)
                self.mValeurs.append(lV)
            
            # écriture des arcs dans les matrice
            for arc in lRows[2:]:
                sd = int(arc[0])
                sa = int(arc[1])
                p = arc[2]
                self.mAdjacence[sd][sa] = True
                self.mValeurs[sd][sa] = p

    # to do: Améliorer l'affichage des matices
    def __str__(self):
        """
            fonction de représentation au format string

            Version 1.0
        """

        s = "Graphe :\n - {0} sommets`\n - {1} arcs\nMatrice d'Adjacence :\n".format(self.nbSommets,self.nbArcs)
        for ligne in self.mAdjacence:
            s+= str(ligne) + '\n'
        s+= 'Matrice des Valeurs :\n'
        for ligne in self.mValeurs:
            s+= str(ligne) + '\n'
        return s
"""
    file : graph.py
    author(s) : Thomas LINTANF, Laurent CALYDON
    Version : 5.0

    Definition de la classe Graph qui permet de stocker un graph orienter et de lui
    appliquer différents algorithmes.
"""

import csv
import logging as log

class Graph :
    """ 
        classe Graph  : représente un graphe orienté 
        
        Version: 4.0
    """

    def __init__(self):
        """ 
            constructeur de la classe Graph

            Version: 4.0
        """

        self.nbSommets = 0
        self.nbArcs = 0
        self.mAdjacence = []
        self.mValeurs = []
        self.contientCircuit = 'u'
        self.rang = []
        self.estOrdonnancement = 'u'
        self.datesAuPlusTot = []
        self.datesAuPlusTard =[]
        self.margesTotales = []
        self.margesLibres = []

    def readFile(self,address):
        """
            Charge un graphe depuis un fichier txt au format csv

            version : 1.3
        """
        lRows = []
        with open(address) as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quoting = csv.QUOTE_NONNUMERIC)
            # stockage temporaire des données dans un tableau
            for row in reader:
                lRows.append([int(i) for i in row])
        log.info('Chargement du fichier : ' + address)

        # extraction du nombre de sommets et d'arcs
        self.nbSommets = int(lRows[0][0])
        log.info('{0} sommets'.format(self.nbSommets))
        self.nbArcs = int(lRows[1][0])
        log.info('{0} arcs'.format(self.nbSommets))

        # Initialisation des matrices d'adjacense et des valeurs
        for si in range(0, self.nbSommets):
            lA = []
            lV = []
            for sJ in range(0, self.nbSommets):
                lA.append(False)
                lV.append('*')
            self.mAdjacence.append(lA)
            self.mValeurs.append(lV)
        log.info('Initialisation des matrices')
        
        # écriture des arcs dans les matrice
        log.info('Chargement des arcs')
        for arc in lRows[2:]:
            sd = int(arc[0])
            sa = int(arc[1])
            p = arc[2]
            self.mAdjacence[sd][sa] = True
            self.mValeurs[sd][sa] = p
            log.info('{0} --> {1} = {2}'.format(sd, sa, p))

    # to do: Améliorer l'affichage des matices
    def __str__(self):
        """
            fonction de représentation au format string

            Version: 1.1
        """

        s = "Graphe :\n - {0} sommets`\n - {1} arcs\nMatrice d'Adjacence :\n".format(self.nbSommets,self.nbArcs)
        for ligne in self.mAdjacence:
            s+= str(ligne) + '\n'
        s+= 'Matrice des Valeurs :\n'
        for ligne in self.mValeurs:
            s+= str(ligne) + '\n'
        return s

    def detectionCircuit(self):
        """
            Cherche si le graphe contient un circuit
            Retourne True si le graphe contient au moins un circuit False sinon
            ecrit également le resultat sur la propriété contient circuit

            Version: 1.2
        """
        
        log.info("Detection de circuit\nMethode de detection des points d'entrer")

        lSommets = list(range(0,self.nbSommets))

        continuer = True
        while(continuer):
            continuer = False
            sToDel = []

            # Recherche des sommets sans prédécesseur
            for sommet in lSommets:
                pred = False
                for s in lSommets:
                    pred = pred | self.mAdjacence[s][sommet]
                
                if(pred == False):
                    sToDel.append(sommet)
            
            # Suppression des sommets sans prédécesseur
            for s in sToDel:
                lSommets.remove(s)
            
            # Sortie de boucle si on a pas retiré de sommets 
            continuer = len(sToDel) > 0 and len(lSommets) > 0

            log.info("Points d'entree :")
            if(continuer):
                log.info(sToDel)
                log.info("Sommets restant :\n{0}".format(lSommets))

            else:
                log.info('Aucun')

        # On regarde si il reste des Sommets pour savoir si il y a un circuit
        self.contientCircuit = len(lSommets) != 0

        if(self.contientCircuit):
            log.info('Le graphe contient au moins un cirvuit')
        else:
            log.info('Le graphe ne contient aucun circuit')

        return self.contientCircuit

    def calcRang(self):
        """
            Calcule le rang de chaque sommet du graphe

            version: 1.2
        """
        
        if self.contientCircuit == 'a':
            log.warning("Impossible de Calculer les rangs : detectionCircuit() doit etre lancer avant")

        elif (self.contientCircuit):
            log.warning("Impossible de Calculer les rangs : presence d'un circuit")
        
        else:
            # Intialisation de la liste des rangs
            for i in range(0, self.nbSommets):
                self.rang.append(0)

            lSommets = list(range(0,self.nbSommets))
            continuer = True
            rang = 0

            while(continuer):
                # Recherche des sommets sans prédécesseur
                sToDel = []
                for sommet in lSommets:
                    pred = False
                    for s in lSommets:
                        pred = pred | self.mAdjacence[s][sommet]
                    
                    if(pred == False):
                        sToDel.append(sommet)

                # Suppression des sommets sans prédécesseur
                for s in sToDel:
                    lSommets.remove(s)
                    self.rang[s] = rang
                
                log.info("Rang courant = {0}\nPoints d'entree :\n{1}".format(rang, sToDel))

                rang+= 1
                continuer = len(lSommets) > 0

            log.info("Graphe vide\nRangs calcules")
            log.info("Sommets\t{0}".format(list(range(0,self.nbSommets))))
            log.info("Rang\t{0}".format(self.rang))

    def estGraphOrdonnancement(self):
        """
            Vérifie si c'est un graphe d'ordonnancement

            Version: 1.2
        """

        log.info("Verification qu'il s'agit d'un graphe d'ordonnancement :")

        #Détection d'un seul point d'entrée
        res = self.rang.count(0) == 1
        log.info("A qu'un seul point d'entree : {0}".format(res))

        #Détection d'un seul point de sortie
        ans = self.rang.count(max(self.rang)) == 1
        log.info("A qu'un seul point de sortie : {0}".format(ans))
        res = res and ans

        #Vérification de la présence d'un circuit
        ans = not self.contientCircuit
        log.info("Ne contient pas un circuit: {0}".format(ans))
        res = res and ans

        #Vérification des valeurs identiques pour tous les arcs incidents vers l’extérieur à un sommet
        ans = True
        for ligne in self.mValeurs:
            i = 0

            while ligne[i] == '*' and i < self.nbSommets-1:
                i+=1

            #Vérification pas d’arcs à valeur négative.
            isPos = True
            if ligne[i] != '*':
                isPos = ligne[i] >= 0
            ans = ans and isPos

            for case in ligne:
                ans = ans and (case == '*' or case == ligne[i] )
        log.info("Arcs incidents exterieurs positifs et egaux pour chaque sommets: {0}".format(ans))
        res = res and ans

        #arcs incidents vers l’extérieur au point d’entrée de valeur nulle
        i = self.rang.index(0)

        ans = True
        for case in self.mValeurs[i]:
            ans = ans and (case == '*' or case == 0 )

        log.info("Arcs incidents exterieurs du point d'entree a valeur 0 : {0}".format(res))
        res = res and ans

        if res :
            log.info("Le graphe est un graphe d'ordonnancement")
        else :
            log.info("Le graphe n'est pas un graphe d'ordonnancement")

        self.estOrdonnancement = res
        return res

    def calcCalendPtot(self):
        """
            Calcule le calendrier au plus tôt si le graphe est un graphe d'ordonnancement

            version: 1.0
        """
        if self.estOrdonnancement == 'u':
            log.error("Le graphe n'as pas ete teste pour l'ordonnancement")

        elif self.estOrdonnancement:
            log.info("Calcul du calendrier au plus tot")

            #Création de la liste des sommets ordonnés par rang croissant
            sommets = []
            for rang in range(0,max(self.rang)+1):
                for sommet in range(0, self.nbSommets):
                    if self.rang[sommet] == rang :
                        sommets.append(sommet)

            # Initialisation du calendrier
            for i in range(self.nbSommets):
                self.datesAuPlusTot.append('*')

            #Date de départ
            i = self.rang.index(0)
            self.datesAuPlusTot[i] = 0
            sommets.remove(i)

            log.info("Sommet 0 date au plus tot : 0")

            for sommet in sommets:
                
                # Construction de la liste des prédécesseurs
                lPred = []
                for pred in range(0, self.nbSommets):
                    if self.mAdjacence[pred][sommet]:
                        lPred.append(pred)
                
                #Calcule des dates par prédécesseurs
                dates = []
                for pred in lPred:
                    dates.append(self.datesAuPlusTot[pred] + self.mValeurs[pred][sommet])
                
                #Calcule de la dates au plus tot
                self.datesAuPlusTot[sommet] = max(dates)
                log.info("Sommet {0} date au plus tot : {1}".format(sommet,self.datesAuPlusTot[sommet]))

            log.info("\nSommets:\t\t{0}\nDates au plus tot:\t{1}".format(list(range(0,self.nbSommets)), self.datesAuPlusTot))

        else:
            log.error("Le graphe n'est pas un graphe d'ordonnancement")

    def calcCalendPtard(self):
        if len(self.datesAuPlusTot) > 0:
            log.info("Calcule du calendrier au plus tard :")

            #Création de la liste des sommets ordonnés par rang décroissant
            sommets = []
            for rang in range(0,max(self.rang)+1):
                for sommet in range(0, self.nbSommets):
                    if self.rang[sommet] == rang :
                        sommets.insert(0,sommet)

            # Initialisation du calendrier
            for i in range(0,self.nbSommets):
                self.datesAuPlusTard.append('*')

            # Date de fin
            f = self.rang.index(max(self.rang))
            self.datesAuPlusTard[f] = self.datesAuPlusTot[f]
            sommets.remove(f)
            log.info("Sommet {0} date au plus tard : {1}".format(f,self.datesAuPlusTard[f]))

            for sommet in sommets:
                # Construction de la liste des successeurs
                lSucc = []
                for succ in range(0, self.nbSommets):
                    if self.mAdjacence[sommet][succ]:
                        lSucc.append(succ)

                #Calcule des dates par successeur
                dates = []
                for succ in lSucc:
                    dates.append(self.datesAuPlusTard[succ] - self.mValeurs[sommet][succ])

                #Calcule de la dates au plus tard
                self.datesAuPlusTard[sommet] = min(dates)
                log.info("Sommet {0} date au plus tard : {1}".format(sommet,self.datesAuPlusTard[sommet]))

            log.info("\nSommets:\t\t{0}\nDates au plus tard:\t{1}".format(list(range(0,self.nbSommets)), self.datesAuPlusTard))
        else:
            log.error("Le calendrier au plus tot n'est pas calculer")
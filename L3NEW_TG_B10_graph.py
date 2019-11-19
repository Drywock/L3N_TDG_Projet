"""
    file : graph.py
    author(s) : Thomas LINTANF, Laurent CALYDON
    Version : 6.0

    Definition de la classe Graph qui permet de stocker un graph orienter et de lui
    appliquer différents algorithmes.
"""

import csv
import logging as log

class Graph:
    """ classe Graph  : représente un graphe orienté Version: 5.0 """

    def __init__(self):
        """
            Constructeur de la classe Graph

            Version: 4.0
        """

        self.nb_sommets = 0
        self.nb_arcs = 0
        self.m_adjacence = []
        self.m_valeurs = []
        self.contient_circuit = 'u'
        self.rang = []
        self.est_ordonnancement = 'u'
        self.dates_au_plus_tot = []
        self.dates_au_plus_tard = []
        self.marges_totales = []
        self.marges_libres = []

    def read_file(self, address):
        """
            Charge un graphe depuis un fichier txt au format csv

            version : 1.3
        """
        l_rows = []
        with open(address) as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            # stockage temporaire des données dans un tableau
            for row in reader:
                l_rows.append([int(i) for i in row])
        log.info('Chargement du fichier : %s', address)

        # extraction du nombre de sommets et d'arcs
        self.nb_sommets = int(l_rows[0][0])
        log.info('%d sommets', self.nb_sommets)
        self.nb_arcs = int(l_rows[1][0])
        log.info('%d arcs', self.nb_sommets)

        # Initialisation des matrices d'adjacense et des valeurs
        for _ in range(0, self.nb_sommets):
            ligne_adjacence = []
            ligne_valeur = []
            for _ in range(0, self.nb_sommets):
                ligne_adjacence.append(False)
                ligne_valeur.append('*')
            self.m_adjacence.append(ligne_adjacence)
            self.m_valeurs.append(ligne_valeur)
        log.info('Initialisation des matrices')

        # écriture des arcs dans les matrice
        log.info('Chargement des arcs')
        for arc in l_rows[2:]:
            sommet_depart = int(arc[0])
            sommet_arrivee = int(arc[1])
            poid = arc[2]
            self.m_adjacence[sommet_depart][sommet_arrivee] = True
            self.m_valeurs[sommet_depart][sommet_arrivee] = poid
            log.info('%d --> %d = %d', sommet_depart, sommet_arrivee, poid)

    # to do: Améliorer l'affichage des matices
    def __str__(self):
        """
            fonction de représentation au format string

            Version: 1.1
        """

        repr_str = "Graphe :\n - {0} sommets`\n - {1} arcs\n".format(self.nb_sommets, self.nb_arcs)
        repr_str += "Matrice d'Adjacence :\n\t"
        for sommet in range(0, self.nb_sommets):
            repr_str += "{0}\t".format(sommet)
        repr_str += '\n'
        indice = 0
        for ligne in self.m_adjacence:
            repr_str += "{0}\t".format(indice)
            for case in ligne:
                repr_str += "{0}\t".format('V' if case else 'F')
            repr_str += '\n'
            indice += 1

        repr_str += 'Matrice des Valeurs :\n'
        repr_str += "\t"
        for sommet in range(0, self.nb_sommets):
            repr_str += "{0}\t".format(sommet)
        repr_str += '\n'

        indice = 0
        for ligne in self.m_valeurs:
            repr_str += "{0}\t".format(indice)
            for case in ligne:
                repr_str += "{0}\t".format(case)
            repr_str += '\n'
            indice += 1
        return repr_str

    def detection_circuit(self):
        """
            Cherche si le graphe contient un circuit
            Retourne True si le graphe contient au moins un circuit False sinon
            ecrit également le resultat sur la propriété contient circuit

            Version: 1.2
        """
        log.info("Detection de circuit\nMethode de detection des points d'entrer")

        liste_sommets = list(range(0, self.nb_sommets))

        continuer = True
        while continuer:
            continuer = False
            sommet_a_supr = []

            # Recherche des sommets sans prédécesseur
            for sommet_arrivee in liste_sommets:
                has_pred = False
                for sommet_depart in liste_sommets:
                    has_pred = has_pred or self.m_adjacence[sommet_depart][sommet_arrivee]

                if not has_pred:
                    sommet_a_supr.append(sommet_arrivee)

            # Suppression des sommets sans prédécesseur
            for sommet in sommet_a_supr:
                liste_sommets.remove(sommet)

            # Sortie de boucle si on a pas retiré de sommets
            continuer = len(sommet_a_supr) > 0 and len(liste_sommets) > 0

            log.info("Points d'entree :")
            if continuer:
                log.info(sommet_a_supr)
                log.info("Sommets restant :\n%s", liste_sommets)

            else:
                log.info('Aucun')

        # On regarde si il reste des Sommets pour savoir si il y a un circuit
        self.contient_circuit = len(liste_sommets) != 0

        if self.contient_circuit:
            log.info('Le graphe contient au moins un cirvuit')
        else:
            log.info('Le graphe ne contient aucun circuit')

        return self.contient_circuit

    def calc_rang(self):
        """
            Calcule le rang de chaque sommet du graphe

            version: 1.2
        """
        if self.contient_circuit == 'u':
            log.warning("Calcule des rangs impossible : detectionCircuit() doit etre lancer avant")

        elif self.contient_circuit:
            log.warning("Impossible de Calculer les rangs : presence d'un circuit")

        else:
            # Intialisation de la liste des rangs
            self.rang = [0 for _ in range(0, self.nb_sommets)]

            liste_sommets = list(range(0, self.nb_sommets))
            continuer = True
            rang = 0

            while continuer:
                # Recherche des sommets sans prédécesseur
                sommet_a_supr = []
                for sommet_arrivee in liste_sommets:
                    has_pred = False
                    for sommet_depart in liste_sommets:
                        has_pred = has_pred or self.m_adjacence[sommet_depart][sommet_arrivee]

                    if not has_pred:
                        sommet_a_supr.append(sommet_arrivee)

                # Suppression des sommets sans prédécesseur
                for sommet in sommet_a_supr:
                    liste_sommets.remove(sommet)
                    self.rang[sommet] = rang

                log.info("Rang courant = %d\nPoints d'entree :\n%s", rang, sommet_a_supr)

                rang += 1
                continuer = len(liste_sommets) > 0

            log.info("Graphe vide\nRangs calcules")
            log.info("Sommets :\t%s", ''.join(["%d\t" % i for i in range(0, self.nb_sommets)]))
            log.info("Rang :\t\t%s", ''.join(["%d\t" % i for i in self.rang]))

    def est_graph_ordonnancement(self):
        """
            Vérifie si c'est un graphe d'ordonnancement

            Version: 1.2
        """

        log.info("Verification qu'il s'agit d'un graphe d'ordonnancement :")

        #Détection d'un seul point d'entrée
        res = self.rang.count(0) == 1
        log.info("A qu'un seul point d'entree : %s", res)

        #Détection d'un seul point de sortie
        ans = self.rang.count(max(self.rang)) == 1
        log.info("A qu'un seul point de sortie : %s", ans)
        res = res and ans

        #Vérification de la présence d'un circuit
        ans = not self.contient_circuit
        log.info("Ne contient pas un circuit: %s", ans)
        res = res and ans

        #Vérification des poids identiques pour tous les arcs incidents vers l’extérieur à un sommet
        ans = True
        for ligne in self.m_valeurs:
            i = 0

            while ligne[i] == '*' and i < self.nb_sommets-1:
                i += 1

            #Vérification pas d’arcs à valeur négative.
            is_pos = True
            if ligne[i] != '*':
                is_pos = ligne[i] >= 0
            ans = ans and is_pos

            for case in ligne:
                ans = ans and (case == '*' or case == ligne[i])
        log.info("Arcs incidents exterieurs positifs et egaux pour chaque sommets: %s", ans)
        res = res and ans

        #arcs incidents vers l’extérieur au point d’entrée de valeur nulle
        i = self.rang.index(0)

        ans = True
        for case in self.m_valeurs[i]:
            ans = ans and (case == '*' or case == 0)

        log.info("Arcs incidents exterieurs du point d'entree a valeur 0 : %s", ans)
        res = res and ans

        if res:
            log.info("Le graphe est un graphe d'ordonnancement")
        else:
            log.info("Le graphe n'est pas un graphe d'ordonnancement")

        self.est_ordonnancement = res
        return res

    def calc_calend_plus_tot(self):
        """
            Calcule le calendrier au plus tôt si le graphe est un graphe d'ordonnancement

            version: 1.0
        """
        if self.est_ordonnancement == 'u':
            log.error("Le graphe n'as pas ete teste pour l'ordonnancement")

        elif self.est_ordonnancement:
            log.info("Calcul du calendrier au plus tot")

            #Création de la liste des sommets ordonnés par rang croissant
            sommets = []
            for rang in range(0, max(self.rang)+1):
                for sommet in range(0, self.nb_sommets):
                    if self.rang[sommet] == rang:
                        sommets.append(sommet)

            # Initialisation du calendrier
            for i in range(self.nb_sommets):
                self.dates_au_plus_tot.append('*')

            #Date de départ
            i = self.rang.index(0)
            self.dates_au_plus_tot[i] = 0
            sommets.remove(i)

            log.info("Sommet 0 date au plus tot : 0")

            for sommet in sommets:
                # Construction de la liste des prédécesseurs
                liste_pred = []
                for pred in range(0, self.nb_sommets):
                    if self.m_adjacence[pred][sommet]:
                        liste_pred.append(pred)

                #Calcule des dates par prédécesseurs
                dates = []
                for pred in liste_pred:
                    dates.append(self.dates_au_plus_tot[pred] + self.m_valeurs[pred][sommet])

                #Calcule de la dates au plus tot
                self.dates_au_plus_tot[sommet] = max(dates)
                log.info("Sommet %d date au plus tot : %d", sommet, self.dates_au_plus_tot[sommet])

            log.info("\nSommets:\t\t\t%s", ''.join('%d\t' % i for i in range(0, self.nb_sommets)))
            log.info("Dates au plus tot:\t%s", ''.join('%s\t' % i for i in self.dates_au_plus_tot))

        else:
            log.error("Le graphe n'est pas un graphe d'ordonnancement")

    def calc_calend_plus_tard(self):
        """
            Calcule du calendrier au plus tard

            version: 1.0
        """
        if len(self.dates_au_plus_tot) > 0:
            log.info("Calcule du calendrier au plus tard :")

            #Création de la liste des sommets ordonnés par rang décroissant
            sommets = []
            for rang in range(0, max(self.rang)+1):
                for sommet in range(0, self.nb_sommets):
                    if self.rang[sommet] == rang:
                        sommets.insert(0, sommet)

            # Initialisation du calendrier
            self.dates_au_plus_tard = ['*' for _ in range(0, self.nb_sommets)]

            # Date de fin
            fin = self.rang.index(max(self.rang))
            self.dates_au_plus_tard[fin] = self.dates_au_plus_tot[fin]
            sommets.remove(fin)
            log.info("Sommet %d date au plus tard : %d", fin, self.dates_au_plus_tard[fin])

            for sommet in sommets:
                # Construction de la liste des successeurs
                liste_succ = []
                for succ in range(0, self.nb_sommets):
                    if self.m_adjacence[sommet][succ]:
                        liste_succ.append(succ)

                #Calcule des dates par successeur
                dates = []
                for succ in liste_succ:
                    dates.append(self.dates_au_plus_tard[succ] - self.m_valeurs[sommet][succ])

                #Calcule de la dates au plus tard
                self.dates_au_plus_tard[sommet] = min(dates)
                log.info("Sommet %d date au plus tard : %d",
                         sommet, self.dates_au_plus_tard[sommet])

            log.info("\nSommets:\t\t\t%s", ''.join('%d\t' % i for i in range(0, self.nb_sommets)))
            log.info("Dates au plus tard:\t%s",
                     ''.join('%d\t' % i for i in self.dates_au_plus_tard))
        else:
            log.error("Le calendrier au plus tot n'est pas calculer")

    def calc_marges(self):
        """
            Calcule les marges totales et libres

            version: 1.1
        """
        # Calcule des marges totales
        log.info("Calcule des marges Totales :")
        for i in range(0, self.nb_sommets):
            self.marges_totales.append(self.dates_au_plus_tard[i] - self.dates_au_plus_tot[i])
            log.info("Sommet %d --> marge totale : %d", i, self.marges_totales[i])

        log.info("\nSommets:\t\t%s", ''.join('%d\t' % i for i in range(0, self.nb_sommets)))
        log.info("Marges Totales:\t%s", ''.join('%d\t' % i for i in self.marges_totales))

        # Calcule des marges libres
        log.info("Calcule des marges Libres :")

        for sommet in range(0, self.nb_sommets - 1):
            # Construction de la liste des successeurs
            liste_succ = []
            for succ in range(0, self.nb_sommets):
                if self.m_adjacence[sommet][succ]:
                    liste_succ.append(succ)

            #calcule de la marge libre par successeur
            marges_libres = []
            for succ in liste_succ:
                marges_libres.append(
                    self.dates_au_plus_tot[succ]
                    - self.dates_au_plus_tot[sommet]
                    - self.m_valeurs[sommet][succ])

            self.marges_libres.append(min(marges_libres))
            log.info("Sommet %d --> marge libre %d", sommet, self.marges_libres[sommet])

        self.marges_libres.append(0)
        log.info("Sommet %d --> marge libre %d",
                 self.nb_sommets-1, self.marges_libres[self.nb_sommets-1])

        log.info("\nSommets:\t\t%s", ''.join('%d\t' % i for i in range(0, self.nb_sommets)))
        log.info("Marges Libres:\t%s", ''.join('%d\t' % i for i in self.marges_libres))

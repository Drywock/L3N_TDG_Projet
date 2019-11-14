import csv

class Graph :

    def __init__(self):
        self.nbSommets = 0
        self.nbArcs = 0
        self.mAdjacence = []
        self.mValeur = []

    def readFile(self,address):
        with open(address) as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quoting = csv.QUOTE_NONNUMERIC)

            lRows = []
            for row in reader:
                lRows.append(row)

            self.nbSommets = int(lRows[0][0])
            self.nbArcs = int(lRows[1][0])

            for si in range(0, self.nbSommets):
                lA = []
                lV = []
                for sJ in range(0, self.nbSommets):
                    lA.append(False)
                    lV.append('*')
                self.mAdjacence.append(lA)
                self.mValeur.append(lV)
            
            for arc in lRows[2:]:
                sd = int(arc[0])
                sa = int(arc[1])
                p = arc[2]
                self.mAdjacence[sd][sa] = True
                self.mValeur[sd][sa] = p
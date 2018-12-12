"""
Le but du projet est de réaliser un résolveur de taquin utilisant A*.
On crée un taquin résoluble, on fait tourner A* dessus avec différentes 
heuristiques, et on compare les résultats.
"""
import math
import copy
from random import randint
import time


# VARIABLES GLOBALES
comptNord,comptSud,comptEst,comptOuest = 0,0,0,0
bestNord,bestSuc,bestOuest,bestEst = 0,0,0,0


# CONSTANTES
POIDS = ((36, 12, 12, 4, 1, 1, 4, 1, 0),    #pi1
        (8, 7, 6, 5, 4, 3, 2, 1, 0),        #pi2 = pi3
        (8, 7, 6, 5, 4, 3, 2, 1, 0),        #pi3 = pi2
        (8, 7, 6, 5, 3, 2, 4, 1, 0),        #pi4 = pi5
        (8, 7, 6, 5, 3, 2, 4, 1, 0),        #pi5 = pi4
        (1, 1, 1, 1, 1, 1, 1, 1, 0))        #pi6

COEFF = (4, 1)  #rho1 à rho6


# CLASSES ET METHODES
class Taquin:
    """Liste des attributs
    
    size : au moins 3
    etat : représentation matricielle par des couples ((abs,ord), valeur)
    Le case est codé par la valeur maximale (size*size - 1)
    chemin : liste des mouvements du case pour parvenir á l'état courant.
    N, S, E, O représentent respectivement Nord, Sud, Est, Ouest.
    Exemples de chemins : 'OSSOSNEEN', 'E', '' (chaîne vide pr état initial)
    cout : cout du chemin actuel. Correspond au nombre de déplacements 
    f : fonction d'évaluation pour A*. f = cout + distanceManhattan
    """

    def __init__(self, n):
        self.size = n
        self.etat = {(j//n, j%n): j for j in range(n*n)}
        self.chemin = ""
        self.cout = 0
        self.f = 0
    
    def afficher(self):
        for i in range(self.size):
            liste = []
            for c in range(self.size):
                liste.append(self.etat[i, c])
            print(liste)


    # Renvoie True si le taquin est résolu.
    def estSoluce(self):
        return self.etat == Taquin(self.size).etat

    # Retourne les coordonnées de la dalle recherchée
    def chercher(self, dalle):
        for i in range(self.size):
            for j in range(self.size):
                if self.etat[(i,j)] == dalle:
                    return (i,j)

    # Déplace le case dans l'une des directions Nord, Sud, Est, Ouest et renvoie le taquin résultant avec le chemin et le cout mis à jour.
    def deplacerCase(self, sens):
        global comptOuest,comptEst,comptSud,comptNord

        copie_T = copy.deepcopy(self)
        case = self.chercher(len(self.etat) - 1)
        if sens == "N":
            copie_T.etat[case] = self.etat[(case[0]-1, case[1])]
            copie_T.etat[(case[0]-1, case[1])] = self.etat[case]
            copie_T.chemin += "N"
            comptNord += 1
        elif sens == "S":
            copie_T.etat[case] = self.etat[(case[0]+1, case[1])]
            copie_T.etat[(case[0]+1, case[1])] = self.etat[case]
            copie_T.chemin += "S"
            comptSud += 1
        elif sens == "E":
            copie_T.etat[case] = self.etat[(case[0], case[1]+1)]
            copie_T.etat[(case[0], case[1]+1)] = self.etat[case]
            copie_T.chemin += "E"
            comptEst += 1
        elif sens == "O":
            copie_T.etat[case] = self.etat[(case[0], case[1]-1)]
            copie_T.etat[(case[0], case[1]-1)] = self.etat[case]
            copie_T.chemin += "O"
            comptOuest += 1
        else:
            print("Mouvement non reconnu. Devrait être N, S, E ou O.")
            print("Ça n'est pas censé se produire.")

        copie_T.cout += 1
        return copie_T


    # Prend un taquin résolu et le mélange avec un grand nombre de mouvements aléatoires. On est sûr qu'il est résolvable en faisant ça.
    def melanger_taquin(self):
        case = list(self.chercher(len(self.etat)-1))

        for i in range(10000):
            caseHaut = (case[0] == 0)
            caseBas = (case[0] == self.size - 1)
            caseGauche = (case[1] == 0)
            caseDroite = (case[1] == self.size - 1)
            caseHG = caseHaut and caseGauche
            caseHD = caseHaut and caseDroite
            caseBG = caseBas and caseGauche
            caseBD = caseBas and caseDroite

            x = randint(1,12)
            if caseHG:
                if x <= 6:
                    self = self.deplacerCase("E")
                    case[1] += 1
                else:
                    self = self.deplacerCase("S")
                    case[0] += 1
            elif caseHD:
                if x <= 6:
                    self = self.deplacerCase("O")
                    case[1] -= 1
                else:
                    self = self.deplacerCase("S")
                    case[0] += 1
            elif caseBG:
                if x <= 6:
                    self = self.deplacerCase("E")
                    case[1] += 1
                else:
                    self = self.deplacerCase("N")
                    case[0] -= 1
            elif caseBD:
                if x <= 6:
                    self = self.deplacerCase("O")
                    case[1] -= 1
                else:
                    self = self.deplacerCase("N")
                    case[0] -= 1
            elif caseHaut:
                if x <= 4:
                    self = self.deplacerCase("O")
                    case[1] -= 1
                elif 4 < x <= 8:
                    self = self.deplacerCase("S")
                    case[0] += 1
                else:
                    self = self.deplacerCase("E")
                    case[1] += 1
            elif caseBas:
                if x <= 4:
                    self = self.deplacerCase("O")
                    case[1] -= 1
                elif 4 < x <= 8:
                    self = self.deplacerCase("N")
                    case[0] -= 1
                else:
                    self = self.deplacerCase("E")
                    case[1] += 1
            elif caseGauche:
                if x <= 4:
                    self = self.deplacerCase("N")
                    case[0] -= 1
                elif 4 < x <= 8:
                    self = self.deplacerCase("E")
                    case[1] += 1
                else:
                    self = self.deplacerCase("S")
                    case[0] += 1
            elif caseDroite:
                if x <= 4:
                    self = self.deplacerCase("N")
                    case[0] -= 1
                elif 4 < x <= 8:
                    self = self.deplacerCase("O")
                    case[1] -= 1
                else:
                    self = self.deplacerCase("S")
                    case[0] += 1
            else:
                if x <= 3:
                    self = self.deplacerCase("N")
                    case[0] -= 1
                elif 3 < x <= 6:
                    self = self.deplacerCase("E")
                    case[1] += 1
                elif 6 < x <= 9:
                    self = self.deplacerCase("S")
                    case[0] += 1
                else:
                    self = self.deplacerCase("O")
                    case[1] -= 1

        # On réinitialise les valeurs car deplacerCase les change
        self.cout = 0
        self.f = 0
        self.chemin = ""
        return self


    # Renvoie une liste des états accessibles à partir de l'état actuel.
    def expanser(self):

        case = self.chercher(len(self.etat) - 1)
        
        caseHaut = (case[0] == 0)
        caseBas = (case[0] == self.size - 1)
        caseGauche = (case[1] == 0)
        caseDroite = (case[1] == self.size - 1)
        caseHG = caseHaut and caseGauche
        caseHD = caseHaut and caseDroite
        caseBG = caseBas and caseGauche
        caseBD = caseBas and caseDroite

        eNord,eSud,eOuest,eEst = None,None,None,None

        if caseHG:
            eEst = self.deplacerCase("E")
            eSud = self.deplacerCase("S")
        elif caseHD:
            eOuest = self.deplacerCase("O")
            eSud = self.deplacerCase("S")
        elif caseBG:
            eNord = self.deplacerCase("N")
            eEst = self.deplacerCase("E")
        elif caseBD:
            eNord = self.deplacerCase("N")
            eOuest = self.deplacerCase("O")
        elif caseHaut:
            eEst = self.deplacerCase("E")
            eSud = self.deplacerCase("S")
            eOuest = self.deplacerCase("O")
        elif caseBas:
            eNord = self.deplacerCase("N")
            eEst = self.deplacerCase("E")
            eOuest = self.deplacerCase("O")
        elif caseGauche:
            eNord = self.deplacerCase("N")
            eSud = self.deplacerCase("S")
            eEst = self.deplacerCase("E")
        elif caseDroite:
            eNord = self.deplacerCase("N")
            eSud = self.deplacerCase("S")
            eOuest = self.deplacerCase("O")
        else:
            eNord = self.deplacerCase("N")
            eSud = self.deplacerCase("S")
            eEst = self.deplacerCase("E")
            eOuest = self.deplacerCase("O")

        return [eNord,eSud,eOuest,eEst]


    # Renvoie le nombre de cases séparant l'élément e de sa position voulue. Fonction intermédiaire pour la distance de Manhattan.
    def dist_elem(self, dalle):
        d = 0

        posActuelle = self.chercher(dalle)
        posDemande = (dalle // self.size, dalle % self.size)
        d = abs(posActuelle[0] - posDemande[0]) + abs(posActuelle[1] - posDemande[1])
        return d


    # Calcule la distance Manhattan avec POIDS[indice] et COEFF[indice].
    # Fonction intermédiaire pour la fonction d'évaluation f.
    def manhattan(self, indice):
        elem = [self.dist_elem(i) for i in range(len(self.etat))]
        elem = tuple(elem) 

        if self.size < 3:
            return sum(POIDS[indice][i] * elem[i] for i in range(len(self.etat))) / COEFF[indice%2]
        else:
            poids = tuple([len(self.etat)-i-1 for i in range(len(self.etat))])
            return sum(poids[i] * elem[i] for i in range(len(self.etat))) / COEFF[indice%2]


    # Fonction de calcul
    def calculer_f(self, indice):
        return self.cout + self.manhattan(indice)


# Liste d'états triés selon leur valeur de f (ordre croissant).
class Frontiere:
    def __init__(self):
        self.etats = []

    # Ajoute e à la bonne position en fonction de sa valeur de f.
    def ajouter(self, etat):
        if self.etats == []:
            self.etats.insert(0,etat)
        else:
            fait = False
            for i in range(len(self.etats)):
                if self.etats[i].f >= etat.f and not fait:
                    self.etats.insert(i,etat)
                    fait = True
            if not fait:
                self.etats.insert(len(self.etats),etat)


# Arbre binaire contenant les états déjà explorés
class DejaExplores:
    def __init__(self):
        self.etats = []

    def ajouter(self, e):
        self.etats.append(e)

    def contient(self, e):
        for i in self.etats:
            if e.etat == i.etat:
                return True
        return False


# ALGORITHME A*
def graph_search():
    # Initialisation =====================================================
    global comptOuest,comptEst,comptSud,comptNord
    t0 = Taquin(int(input("Entrer la taille du taquin : ")))
    pond = int(input("Pondération pour les distances de Manhattan (0 à 5) : "))

    t0 = t0.melanger_taquin() #pour avoir un taquin non résolu
    #print(t0.etat) #affiche le taquin initial
    t0.afficher()
    print("\n**************************************************\n")
    for pond in range(2):
        t = t0
        frontiere = Frontiere()
        frontiere.ajouter(t0)
        historique = DejaExplores() #crée l'ensemble des états déjà explorés

        if t0.estSoluce():
            print("Le taquin est déjà solution.")
            return ""
        

        start_time = time.time()
    # Boucle principale =================================================
        while not t.estSoluce():

            if len(frontiere.etats) == 0:
                return "Aucune solution"

            t = frontiere.etats.pop(0)
            if t.estSoluce():
                print("Recherche terminée en %s secondes" % (time.time() - start_time))
                print("Solution : " + str(t.chemin))
                print(str(len(historique.etats)) + " états explorés\n")  
                """t.afficher()"""
                print("Nombre total de déplacements vers le Nord : " + str(comptNord) + "\n")
                print("Nombre total de déplacements vers le Sud : " + str(comptSud) + "\n")
                print("Nombre total de déplacements vers l'Ouest : " + str(comptOuest) + "\n")
                print("Nombre total de déplacements vers l'Est : " + str(comptEst) + "\n")
                print("**************************************************\n")
                comptNord,comptSud,comptEst,comptOuest = 0,0,0,0
            else:
                if t.chemin != "":
                    t.chemin += " / "

            # On récupère une liste des états accessibles
            expansion = t.expanser()
            historique.ajouter(t)
            for i in range(len(expansion)):
                if not expansion[i] == None:
                    expansion[i].f = expansion[i].calculer_f(pond)
                    if not historique.contient(expansion[i]):
                        frontiere.ajouter(expansion[i])
    return 0

graph_search()

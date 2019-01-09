"""
Titre :
    - taquin.py
Execution :
    - Depuis un terminal (linux) : python3 taquin.py
Description :
    - L’objectif consiste à déterminer le nombre minimal de déplacements,
        nécessaire pour passer d’un taquin quelconque vers un taquin solution.
    - L'objectif final sera de proposer l’étude des taquins 4 × 4.
Auteurs :
    - Ronan LAMPE
    - Romain TONDEUR
    - Amine MESSAOUDI
"""

import math
import copy
from random import randint
import time


# VARIABLES GLOBALES
totalHaut, totalBas, totalDroite, totalGauche = 0, 0, 0, 0
bestHaut, bestBas, bestGauche, bestDroite = math.inf, math.inf, math.inf, math.inf


# CONSTANTES
POIDS = ((36, 12, 12, 4, 1, 1, 4, 1, 0),    # pi1
        (8, 7, 6, 5, 4, 3, 2, 1, 0),        # pi2 = pi3
        (8, 7, 6, 5, 4, 3, 2, 1, 0),        # pi3 = pi2
        (8, 7, 6, 5, 3, 2, 4, 1, 0),        # pi4 = pi5
        (8, 7, 6, 5, 3, 2, 4, 1, 0),        # pi5 = pi4
        (1, 1, 1, 1, 1, 1, 1, 1, 0))        # pi6

COEFF = (4, 1)  # rho1 à rho6


# CLASSES ET METHODES
class Taquin:

    # Attributs
    def __init__(self, n):
        # Taille du taquin (au moins 3)
        self.size = n

        # Représentation matricielle du taquin par des tuples ((abs,ord), valeur)
        # La case vide est codée par la valeur maximale (size*size - 1)
        self.etat = {(j // n, j % n): j for j in range(n*n)}

        # Historique des déplacements de la case vide jusqu'à l'état courant.
        # Chaque caractère représente un déplacement (Haut, Bas, Droite, Gauche)
        # Exemples : "GBBGBHDDH", "D", "" (chaîne vide étant l'état initial)
        self.chemin = ""

        # Compteurs des déplacements
        self.comptHaut = 0
        self.comptBas = 0
        self.comptDroite = 0
        self.comptGauche = 0

        # Coût du chemin actuel, il correspond au nombre de déplacements
        self.cout = 0

        # Fonction d'évaluation pour l'algorithme A* (f = cout + distanceManhattan)
        self.f = 0

    # Affiche le taquin
    def afficher(self):
        for i in range(self.size):
            liste = []
            for j in range(self.size):
                liste.append(self.etat[i, j])
            print(liste)

    # Retourne l'état du taquin (True = Résolu | False = Non résolu)
    def estSoluce(self):
        return self.etat == Taquin(self.size).etat

    # Retourne les coordonnées de la case recherchée
    def rechercher(self, dalle):
        for i in range(self.size):
            for j in range(self.size):
                if self.etat[(i, j)] == dalle:
                    return i, j

    # Déplace la case vide dans une direction (Haut, Bas, Droite, Gauche)
    def deplacer(self, direction):
        # On récupère l'accès au variables globales
        global totalGauche, totalDroite, totalBas, totalHaut
        global comptGauche, comptDroite, comptBas, comptHaut

        # On crée une copie du taquin
        copie_taquin = copy.deepcopy(self)

        # On recherche les coordonnées de la case vide
        case_vide = self.rechercher(len(self.etat) - 1)

        # On déplace la case vide dans la direction donnée
        if direction == "H":
            # On permute la case vide avec la case du haut
            copie_taquin.etat[(case_vide[0]-1, case_vide[1])] = self.etat[case_vide]
            copie_taquin.etat[case_vide] = self.etat[(case_vide[0]-1, case_vide[1])]

            # On met à jour l'historique
            copie_taquin.chemin += "H"

            # On met à jour les indicateurs
            totalHaut += 1
            copie_taquin.comptHaut += 1
        elif direction == "B":
            # On permute la case vide avec la case du bas
            copie_taquin.etat[(case_vide[0]+1, case_vide[1])] = self.etat[case_vide]
            copie_taquin.etat[case_vide] = self.etat[(case_vide[0]+1, case_vide[1])]

            # On met à jour l'historique
            copie_taquin.chemin += "B"

            # On met à jour les indicateurs
            totalBas += 1
            copie_taquin.comptBas += 1
        elif direction == "D":
            # On permute la case vide avec la case de droite
            copie_taquin.etat[(case_vide[0], case_vide[1]+1)] = self.etat[case_vide]
            copie_taquin.etat[case_vide] = self.etat[(case_vide[0], case_vide[1]+1)]

            # On met à jour l'historique
            copie_taquin.chemin += "D"

            # On met à jour les indicateurs
            totalDroite += 1
            copie_taquin.comptDroite += 1
        elif direction == "G":
            # On permute la case vide avec la case de gauche
            copie_taquin.etat[(case_vide[0], case_vide[1]-1)] = self.etat[case_vide]
            copie_taquin.etat[case_vide] = self.etat[(case_vide[0], case_vide[1]-1)]

            # On met à jour l'historique
            copie_taquin.chemin += "G"

            # On met à jour les indicateurs
            totalGauche += 1
            copie_taquin.comptGauche += 1
        else:
            print("Déplacement non reconnu. Devrait être H, B, D ou G.")

        copie_taquin.cout += 1
        return copie_taquin

    # Mélange le taquin but tout en le gardant résoluble (grand nb de déplacements aléatoires)
    def melanger_taquin(self):
        # On récupère l'accès au variables globales
        global totalGauche, totalDroite, totalBas, totalHaut

        # On recherche les coordonnées de la case vide
        case_vide = list(self.rechercher(len(self.etat)-1))

        # Pour 10000 itérations
        for _ in range(10000):
            # On génére un entier compris entre 1 et 12
            x = randint(1, 12)

            # On défini les booléens pour la position de la case vide
            vide_haut = (case_vide[0] == 0)
            vide_bas = (case_vide[0] == self.size - 1)
            vide_droite = (case_vide[1] == self.size - 1)
            vide_gauche = (case_vide[1] == 0)
            vide_haut_gauche = vide_haut and vide_gauche
            vide_haut_droite = vide_haut and vide_droite
            vide_bas_gauche = vide_bas and vide_gauche
            vide_bas_droite = vide_bas and vide_droite

            # On déplace la case vide selon l'entier généré
            if vide_haut_gauche:
                if x <= 6:
                    case_vide[1] += 1
                    self = self.deplacer("D")
                else:
                    case_vide[0] += 1
                    self = self.deplacer("B")
            elif vide_haut_droite:
                if x <= 6:
                    case_vide[1] -= 1
                    self = self.deplacer("G")
                else:
                    case_vide[0] += 1
                    self = self.deplacer("B")
            elif vide_bas_gauche:
                if x <= 6:
                    case_vide[1] += 1
                    self = self.deplacer("D")
                else:
                    case_vide[0] -= 1
                    self = self.deplacer("H")
            elif vide_bas_droite:
                if x <= 6:
                    case_vide[1] -= 1
                    self = self.deplacer("G")
                else:
                    case_vide[0] -= 1
                    self = self.deplacer("H")
            elif vide_haut:
                if x <= 4:
                    case_vide[1] -= 1
                    self = self.deplacer("G")
                elif 4 < x <= 8:
                    case_vide[0] += 1
                    self = self.deplacer("B")
                else:
                    case_vide[1] += 1
                    self = self.deplacer("D")
            elif vide_bas:
                if x <= 4:
                    case_vide[1] -= 1
                    self = self.deplacer("G")
                elif 4 < x <= 8:
                    case_vide[0] -= 1
                    self = self.deplacer("H")
                else:
                    case_vide[1] += 1
                    self = self.deplacer("D")
            elif vide_gauche:
                if x <= 4:
                    case_vide[0] -= 1
                    self = self.deplacer("H")
                elif 4 < x <= 8:
                    case_vide[1] += 1
                    self = self.deplacer("D")
                else:
                    case_vide[0] += 1
                    self = self.deplacer("B")
            elif vide_droite:
                if x <= 4:
                    case_vide[0] -= 1
                    self = self.deplacer("H")
                elif 4 < x <= 8:
                    case_vide[1] -= 1
                    self = self.deplacer("G")
                else:
                    case_vide[0] += 1
                    self = self.deplacer("B")
            else:
                if x <= 3:
                    case_vide[0] -= 1
                    self = self.deplacer("H")
                elif 3 < x <= 6:
                    case_vide[1] += 1
                    self = self.deplacer("D")
                elif 6 < x <= 9:
                    case_vide[0] += 1
                    self = self.deplacer("B")
                else:
                    case_vide[1] -= 1
                    self = self.deplacer("G")

        # On réinitialise les valeurs car changées par deplacer()
        self.cout, self.f, self.chemin = 0, 0, ""
        totalHaut, totalBas, totalDroite, totalGauche = 0, 0, 0, 0
        self.comptHaut, self.comptBas, self.comptDroite, self.comptGauche = 0, 0, 0, 0

        # On retourne le taquin mélangé
        return self

    # Retourne la liste des états accessibles à partir de l'état actuel
    def etendre(self):

        # On recherche les coordonnées de la case vide
        case_vide = self.rechercher(len(self.etat) - 1)

        # On défini les booléens pour la position de la case vide
        vide_haut = (case_vide[0] == 0)
        vide_bas = (case_vide[0] == self.size - 1)
        vide_droite = (case_vide[1] == self.size - 1)
        vide_gauche = (case_vide[1] == 0)
        vide_haut_gauche = vide_haut and vide_gauche
        vide_haut_droite = vide_haut and vide_droite
        vide_bas_gauche = vide_bas and vide_gauche
        vide_bas_droite = vide_bas and vide_droite

        # On initialise les états accessibles
        etat_haut, etat_bas, etat_gauche, etat_droite = None, None, None, None

        # On déplace la case vide dans les directions disponibles
        if vide_haut_gauche:
            etat_bas = self.deplacer("B")
            etat_droite = self.deplacer("D")
        elif vide_haut_droite:
            etat_bas = self.deplacer("B")
            etat_gauche = self.deplacer("G")
        elif vide_bas_gauche:
            etat_haut = self.deplacer("H")
            etat_droite = self.deplacer("D")
        elif vide_bas_droite:
            etat_haut = self.deplacer("H")
            etat_gauche = self.deplacer("G")
        elif vide_haut:
            etat_bas = self.deplacer("B")
            etat_droite = self.deplacer("D")
            etat_gauche = self.deplacer("G")
        elif vide_bas:
            etat_haut = self.deplacer("H")
            etat_droite = self.deplacer("D")
            etat_gauche = self.deplacer("G")
        elif vide_gauche:
            etat_bas = self.deplacer("B")
            etat_haut = self.deplacer("H")
            etat_droite = self.deplacer("D")
        elif vide_droite:
            etat_bas = self.deplacer("B")
            etat_haut = self.deplacer("H")
            etat_gauche = self.deplacer("G")
        else:
            etat_bas = self.deplacer("B")
            etat_haut = self.deplacer("H")
            etat_droite = self.deplacer("D")
            etat_gauche = self.deplacer("G")

        # On retourne les états accessibles
        return [etat_haut, etat_bas, etat_droite, etat_gauche]

    # Retourne le nombre de cases séparant la case donnée de sa position but.
    def dist_elem(self, case):

        # On recherche la position actuelle de la case
        pos_actuelle = self.rechercher(case)

        # On déduit la position but
        pos_but = (case // self.size, case % self.size)

        # On calcule la distance
        distance = abs(pos_actuelle[0] - pos_but[0]) + abs(pos_actuelle[1] - pos_but[1])

        return distance

    # Fonction de calcul de la distance Manhattan
    def manhattan(self, ponderation):

        elem = [self.dist_elem(i) for i in range(len(self.etat))]
        elem = tuple(elem) 

        if self.size < 3:
            return sum(POIDS[ponderation][i] * elem[i] for i in range(len(self.etat))) / COEFF[ponderation % 2]
        else:
            poids = tuple([len(self.etat)-i-1 for i in range(len(self.etat))])
            return sum(poids[i] * elem[i] for i in range(len(self.etat))) / COEFF[ponderation % 2]

    # Fonction de calcul de f
    def calculer_f(self, ponderation):
        return self.cout + self.manhattan(ponderation)


# Liste d'états triés selon f (croissant)
class Frange:
    def __init__(self):
        self.etats = []

    # Ajoute l'état en fonction de son f
    def ajouter(self, etat):
        if not self.etats:
            self.etats.insert(0, etat)
        else:
            fait = False
            for i in range(len(self.etats)):
                if self.etats[i].f >= etat.f and not fait:
                    self.etats.insert(i, etat)
                    fait = True
            if not fait:
                self.etats.insert(len(self.etats), etat)


# Arbre binaire qui contient les taquins explorés
class DejaExplores:
    def __init__(self):
        self.taquins = []

    def ajouter(self, taquin):
        self.taquins.append(taquin)

    def contient(self, taquin):
        for taq in self.taquins:
            if taquin.etat == taq.etat:
                return True
        return False


# Retourne un taquin initialisé et mélangé
def init_taquin():
    taquin = Taquin(int(input("Veuillez indiquer la taille du taquin : ")))

    # On affiche le taquin but
    print("\nTaquin but:")
    taquin.afficher()

    # On mélange le taquin but (résoluble)
    taquin = taquin.melanger_taquin()

    # On affiche le taquin initial
    print("\nTaquin initial:")
    taquin.afficher()

    return taquin


# Algorithme de recherche A*
def rech_taquin(taquin):
    # On récupère l'accès au variables globales
    global totalGauche, totalDroite, totalBas, totalHaut
    global bestDroite, bestGauche, bestBas, bestHaut

    # On récupère la pondération pour Manhattan
    ponderation = int(input("\nPondération pour les distances de Manhattan (0 à 5) : "))

    for pond in range(ponderation):
        print("\n***************** Ponderation : " + str(pond) + " *****************\n")

        # On crée une copie du taquin
        taq = taquin

        # On crée la frange
        frange = Frange()
        frange.ajouter(taquin)

        # On crée l'historique des taquins explorés
        historique = DejaExplores()

        # On vérifie que le taquin initial ne soit pas déjà résolu
        if taquin.estSoluce():
            print("Le taquin est déjà solution.")
            return ""

        # On démarre le timer
        start_time = time.time()

        while not taq.estSoluce():

            # Si la frange ne contient aucun etat, alors il n'y a aucune solution
            if len(frange.etats) == 0:
                return "Aucune solution"

            # On vérifie si le taquin but à été atteint
            taq = frange.etats.pop(0)
            if taq.estSoluce():

                # Si oui, on affiche nos indicateurs
                print("Recherche terminée en %s secondes" % (time.time() - start_time))
                print("Solution : " + str(taq.chemin))
                print("Coût : " + str(taq.cout))
                print(str(len(historique.taquins)) + " taquins explorés\n")

                print("---------------------------------------------------\n")
                print("Nombre de déplacements vers le Haut : " + str(taq.comptHaut) + "\n")
                print("Nombre de déplacements vers le Bas : " + str(taq.comptBas) + "\n")
                print("Nombre de déplacements vers la Gauche : " + str(taq.comptGauche) + "\n")
                print("Nombre de déplacements vers la Droite : " + str(taq.comptDroite) + "\n")
                print("---------------------------------------------------\n")
                print("Nombre total de déplacements vers le Haut : " + str(totalHaut) + "\n")
                print("Nombre total de déplacements vers le Bas : " + str(totalBas) + "\n")
                print("Nombre total de déplacements vers la Gauche : " + str(totalGauche) + "\n")
                print("Nombre total de déplacements vers la Droite : " + str(totalDroite) + "\n")
                # print("**************************************************\n")
                # print("Nombre de déplacements vers le Haut pour le meilleur test : " + str(bestHaut) + "\n")
                # print("Nombre de déplacements vers le Bas pour le meilleur test : " + str(bestBas) + "\n")
                # print("Nombre de déplacements vers la Droite pour le meilleur test : " + str(bestDroite) + "\n")
                # print("Nombre de déplacements vers la Gauche pour le meilleur test : " + str(bestGauche) + "\n")

                # On réinitialise une partie de nos indicateurs
                totalHaut, totalBas, totalDroite, totalGauche = 0, 0, 0, 0
            else:
                if taq.chemin != "":
                    taq.chemin += " / "

            # On récupère les états accessibles depuis le taquin
            extension = taq.etendre()
            historique.ajouter(taq)

            for indice in range(len(extension)):
                if extension[indice]:
                    extension[indice].f = extension[indice].calculer_f(pond)
                    if not historique.contient(extension[indice]):
                        frange.ajouter(extension[indice])

            # On met à jour les indicateurs
            # if taq.comptHaut < bestHaut:
            #    bestHaut = taq.comptHaut
            # if taq.comptBas < bestBas:
            #    bestBas = taq.comptBas
            # if taq.comptDroite < bestDroite:
            #    bestDroite = taq.comptDroite
            # if taq.comptGauche < bestGauche:
            #    bestGauche = taq.comptGauche
    return 0


# On crée un taquin résoluble, auquel on applique l'algorithme A* selon différentes heuristiques
rech_taquin(init_taquin())

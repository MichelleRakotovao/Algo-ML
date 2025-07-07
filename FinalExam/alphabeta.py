import random
import csv

class alphabeta:

    etat_unique = set()

    @staticmethod
    def verification_Winner (plateau):
        combinaison_winner = [
         [0, 1, 2], [0, 3, 6], [0, 4, 8], [1, 4, 7], [3, 4, 5], [2, 4, 6], [6, 7, 8], [2, 5, 8]
         ]

        for combinaison in combinaison_winner:
         a, b, c = combinaison

         if plateau[a] !=0 and plateau[a] == plateau[b] == plateau[c]:
            return plateau[a]
         
        return 0
    
    @staticmethod
    def filtrage_symetrique(plateau):
        grille = [plateau[0:3], plateau[3:6], plateau[6:9]]

        def rotation_90(mat):
            return [list(row) for row in zip(*mat[::-1])]

        def miroir_horizontal(mat):
            return mat[::1]

        def miroir_vertical(mat):
            return [row[::-1] for row in mat]
        
        def flatten(mat):
            return [case for ligne in mat for case in ligne]
        
        formes = []
        temp = grille
        for _ in range(4): 
            formes.append(flatten(temp))
            formes.append(flatten(rotation_90(temp)))
            formes.append(flatten(miroir_horizontal(temp)))
            formes.append(flatten(miroir_vertical(temp)))
        return formes

    @classmethod
    def generation_etat_valide(cls):
        while True :
            plateau = [0] * 9
            nombre_de_coups = random.randint(2, 8)
            joueur_actuel = 1
            position_disponibles = list(range(9))

            for _ in range(nombre_de_coups):
                if not position_disponibles:
                    break
                case = random.choice(position_disponibles)
                plateau[case] = joueur_actuel
                position_disponibles.remove(case)
                joueur_actuel *= -1

            nombre_x = plateau.count(1)
            nombre_o = plateau.count(-1)
            gagnant = cls.verification_Winner(plateau)

            if abs(nombre_x - nombre_o) <= 1 and gagnant == 0:
                est_deja_vu = False
                for sym in cls.filtrage_symetrique(plateau):
                    if tuple(sym) in cls.etat_unique:
                        est_deja_vu = True
                        break

                if not est_deja_vu :
                    cls.etat_unique.add(tuple(plateau))
                    prochain_joueur = 1 if nombre_x == nombre_o else -1
                    return plateau, prochain_joueur, nombre_de_coups
            
    @staticmethod
    def est_plein(plateau):
        return all(cell != 0 for cell in plateau)
    
    @staticmethod
    def coup_possible(plateau):
        return [i for i, val in enumerate(plateau) if val == 0]
    
    @staticmethod
    def evaluate(plateau):
        return alphabeta.verification_Winner(plateau)
    
    @staticmethod
    def minimax(plateau, joueur, alpha, beta):
        gagnant = alphabeta.evaluate(plateau)
        if gagnant != 0:
            return gagnant * joueur, None
        if alphabeta.est_plein(plateau):
            return 0, None
        
        meilleur_score = -float('inf')
        meilleur_coup = None

        for coup in alphabeta.coup_possible(plateau):
            plateau[coup]  = joueur
            score, _ = alphabeta.minimax(plateau, -joueur, -beta, -alpha)
            score = -score
            plateau[coup] = 0

            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = coup

            alpha = max(alpha, score)
            if alpha >= beta:
                break

        return  meilleur_score, meilleur_coup
    
def analyser_etats(etats):
    dataset = []
    for plateau, joueur, coups in etats:
        score, meilleur_coup = alphabeta.minimax(plateau[:], joueur, -float('inf'), float('inf'))
        ligne = plateau + [joueur, meilleur_coup]
        dataset.append(ligne)
    return dataset

def exporter_csv(dataset, nom_fichier="datasetMorpion.csv"):
    with open(nom_fichier, mode='w', newline='') as fichier:
        writer = csv.writer(fichier)
        headers = [f"c{i}" for i in range(9)] + ["joueur", "best_move"]
        writer.writerow(headers)
        for lignes in dataset:
            writer.writerow(lignes)

if __name__ == "__main__":
    print(" Génération des états...")
    etats = [alphabeta.generation_etat_valide() for _ in range(500)] 
    
    print(" Analyse par Minimax...")
    analyse = analyser_etats(etats)
    
    print(" Export du dataset CSV...")
    exporter_csv(analyse, "dataset_tictactoe.csv")
    
    print("Fichier 'dataset_tictactoe.csv' généré avec succès.")

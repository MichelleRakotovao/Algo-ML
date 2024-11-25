import random
import heapq
import csv
from time import time

class Matrices:
    def current_matrix(self, n):
        #-- Génère une matrice initiale aléatoire et solvable.
        values = [i + 1 for i in range(n * n - 1)] + [0] #generation matrice [0+1 ,1+1 , ..... ]+[0]
        while True:
            random.shuffle(values) #Mélange la liste
            if self.is_solvable(values, n):
                break
        return [values[i:i + n] for i in range(0, len(values), n)] #decoupage du matrice --> produit : [0, 3, 6]

# values = [1, 2, 3, 4, 5, 6, 7, 8, 0]
# matrice = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 0]
# ]


    def end_matrix(self, n):
        # -- Génère la matrice finale
        values = [i + 1 for i in range(n * n - 1)] + [0]
        return [values[i:i + n] for i in range(0, len(values), n)]


#onditions de solvabilité :
    #Puzzle avec une grille de dimensions impaires (n%2=1)
    #Le puzzle est résolvable si le nombre total d'inversions est pair.
        #Une inversion est une paire de tuiles (𝑎,𝑏) avec 𝑎>𝑏 où 𝑎 apparaît avant b dans l'ordre linéaire du puzzle.

#Puzzle avec une grille de dimensions paires (n%2=0)
    #(nombre d’inversions + ligne du zero)%2=0


#Inversion : Une paire  (a,b) est une inversion si a apparaît avant b dans values, mais a>b (sauf si b=0, car 0 représente une case vide).
    def is_solvable(self, values, n):
        # Vérifie si une configuration de puzzle est solvable.
        inversions = sum(
            1 for i in range(len(values)) for j in range(i + 1, len(values))
            if values[i] > values[j] > 0
        )
        if n % 2 == 1:  # Dimensions impaires
            return inversions % 2 == 0
        else:  # Dimensions paires
            row_empty = values.index(0) // n
            return (inversions + row_empty) % 2 == 0

    #manhattan_distance = ∣x1−x2∣+∣y1−y2∣
    def manhattan_distance(self, etat, goal, n):
        # Calcule la distance de Manhattan entre deux états.
        distance = 0
        for i in range(n):
            for j in range(n):
                value = etat[i][j]
                if value != 0:
                    goal_x, goal_y = divmod(goal.index(value), n)
                    distance += abs(i - goal_x) + abs(j - goal_y)
        return distance


    def get_neighbors(self, etat, n, swap_type="standard", swap_count=1):
        # Génère les voisins selon le type de swap spécifié."""
        flat_etat = sum(etat, [])
        neighbors = []

        if swap_type == "0-swap":
            # Aucun mouvement autorisé
            return []

        elif swap_type == "dynamic":
            # Générer des permutations aléatoires selon le nombre de swaps spécifié
            for _ in range(swap_count):
                new_flat = flat_etat[:]
                idx1, idx2 = random.sample(range(len(new_flat)), 2)
                new_flat[idx1], new_flat[idx2] = new_flat[idx2], new_flat[idx1]
                neighbors.append([new_flat[i:i + n] for i in range(0, len(new_flat), n)])
            return neighbors

        # Cas standard : mouvement de la case vide
        x, y = divmod(flat_etat.index(0), n)
         
        # déplcement de Droite, gauche, bas, haut
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                new_flat = flat_etat[:]
                new_flat[x * n + y], new_flat[nx * n + ny] = new_flat[nx * n + ny], new_flat[x * n + y]
                neighbors.append([new_flat[i:i + n] for i in range(0, len(new_flat), n)])
        return neighbors
    
    # -- Exporte les valeurs dans un fichier CSV
    def export_results_to_csv(filename, data):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def solve_puzzle(self, initial, goal, n, swap_type="standard", swap_count=1):
        #-- Résoud le puzzle avec l'algorithme A* pour un type de swap donné.
        frontier = []
        heapq.heappush(frontier, (0, initial, 0, None))
        explored = set()
        came_from = {}

        flat_goal = sum(goal, [])  # Aplatie la matrice goal pour la comparaison
        while frontier:
            f, current, g, parent = heapq.heappop(frontier)

            current_tuple = tuple(map(tuple, current))
            if current_tuple in explored:
                continue

            came_from[current_tuple] = parent
            explored.add(current_tuple)

            # Vérifier si la solution est trouvée
            if sum(current, []) == flat_goal:  # Aplatie la matrice actuelle pour la comparaison
                path = []
                while current:
                    path.append(current)
                    current = came_from[tuple(map(tuple, current))]
                return path[::-1]

            for neighbor in self.get_neighbors(current, n, swap_type, swap_count):
                neighbor_tuple = tuple(map(tuple, neighbor))
                if neighbor_tuple not in explored:
                    h = self.manhattan_distance(neighbor, flat_goal, n)  
                    heapq.heappush(frontier, (g + 1 + h, neighbor, g + 1, current))
        return None

    @staticmethod
    def print_matrix(matrix):
        # Affiche une matrice
        for row in matrix:
            print(" ".join(f"{val:3}" for val in row))
        print()

# -- Programme test
if _name_ == "_main_":
    dimension = int(input("Choisir la dimension (3 ou 4) : "))
    swap_type = input("Choisir le type de swap (standard, 0-swap, dynamic) : ").strip().lower()
    swap_count = 1  # Par défaut, un seul swap dynamique

    if swap_type == "dynamic":
        swap_count = int(input("Spécifiez le nombre de swaps dynamiques : "))

    if dimension in {3, 4} and swap_type in {"standard", "0-swap", "dynamic"}:
        matrices = Matrices()
        print("\nMatrice initiale :")
        start_matrix = matrices.current_matrix(dimension)
        matrices.print_matrix(start_matrix)

        print("\nMatrice finale :")
        goal_matrix = matrices.end_matrix(dimension)
        matrices.print_matrix(goal_matrix)

        print("\nRésolution du puzzle :")
        start_time = time()
        solution = matrices.solve_puzzle(start_matrix, goal_matrix, dimension, swap_type=swap_type, swap_count=swap_count)
        end_time = time()

        execution_time = end_time - start_time
        if solution:
            print(f"Solution trouvée en {len(solution) - 1} étapes.")
            for step_num, step in enumerate(solution):
                print(f"\nÉtape {step_num + 1} :")
                matrices.print_matrix(step)
        else:
            print("Aucune solution trouvée.")

        # Collecte des données pour export
        result = {
            "Dimension": dimension,
            "Swap Type": swap_type,
            "Swap Count": swap_count if swap_type == "dynamic" else None,
            "Execution Time (s)": execution_time,
            "Moves": len(solution) - 1 if solution else None,
            "Status": "Success" if solution else "Failed",
        }

        # Export des résultats
        Matrices.export_results_to_csv("solver_results.csv", [result])
        print("Les résultats ont été exportés vers 'solver_results.csv'.")
    else:
        print("Veuillez choisir une dimension valide (3 ou 4) et un type de swap correct (standard, 0-swap, dynamic).")
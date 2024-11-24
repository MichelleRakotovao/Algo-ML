import random
import heapq

class Matrices:

    def current_matrix(self, n):
        
        #-- Génère une matrice initiale aléatoire et valide pour le puzzle.
        values = [i + 1 for i in range(n * n - 1)] + [0]
        while True:
            random.shuffle(values)
            if self.is_solvable(values, n):
                break
        return [values[i:i + n] for i in range(0, len(values), n)]

    def end_matrix(self, n):
        # -- Génère la matrice finale du puzzle.
        
        values = [i + 1 for i in range(n * n - 1)] + [0]
        return [values[i:i + n] for i in range(0, len(values), n)]

    def is_solvable(self, values, n):
        
        # -- Vérifie si la configuration initiale du puzzle est solvable.
        
        inversions = sum(
            1 for i in range(len(values)) for j in range(i + 1, len(values))
            if values[i] > values[j] > 0
        )
        if n % 2 == 1:  # Dimensions impaires
            return inversions % 2 == 0
        else:  # Dimensions paires
            row_empty = values.index(0) // n
            return (inversions + row_empty) % 2 == 0

    def manhattan_distance(self, etat, goal, n):
        # -- Calcule la distance de Manhattan entre l'état actuel et l'état final.
        distance = 0
        flat_etat = sum(etat, [])
        for index, value in enumerate(flat_etat):
            if value != 0:
                goal_index = goal.index(value)
                current_x, current_y = divmod(index, n)
                goal_x, goal_y = divmod(goal_index, n)
                
                distance += abs(current_x - goal_x) + abs(current_y - goal_y)
        return distance

    def get_neighbors(self, etat, n, swap_type="standard"):
       #-- Génère les voisins de l'état courant selon la règle de swap spécifiée.
        
        if swap_type == "0-swap":
            # Aucun mouvement autorisé
            return []

        flat_etat = sum(etat, [])
        neighbors = []

        if swap_type == "10-swap":
            # Générer jusqu'à 10 permutations aléatoires
            for _ in range(10):
                new_flat = flat_etat[:]
                idx1, idx2 = random.sample(range(len(new_flat)), 2)
                new_flat[idx1], new_flat[idx2] = new_flat[idx2], new_flat[idx1]
                neighbors.append([new_flat[i:i + n] for i in range(0, len(new_flat), n)])
            return neighbors

        # Comportement standard : mouvement de la case vide
        x, y = divmod(flat_etat.index(0), n)
        # Déplacement de droite, gauche, bas, haut
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                new_flat = flat_etat[:]
                new_flat[x * n + y], new_flat[nx * n + ny] = new_flat[nx * n + ny], new_flat[x * n + y]
                neighbors.append([new_flat[i:i + n] for i in range(0, len(new_flat), n)])
        return neighbors

    def solve_puzzle(self, initial, goal, n, swap_type="standard"):
        # -- Résoud le puzzle en utilisant l'algorithme A* avec une règle de swap spécifiée.
        
        frontier = []
        heapq.heappush(frontier, (0, initial, 0, None))
        explored = set()
        came_from = {}

        flat_goal = sum(goal, [])
        while frontier:
            f, current, g, parent = heapq.heappop(frontier)

            current_tuple = tuple(map(tuple, current))
            if current_tuple in explored:
                continue

            came_from[current_tuple] = parent
            explored.add(current_tuple)

            if sum(current, []) == flat_goal:
                path = []
                while current:
                    path.append(current)
                    current = came_from[tuple(map(tuple, current))]
                return path[::-1]

            for neighbor in self.get_neighbors(current, n, swap_type):
                neighbor_tuple = tuple(map(tuple, neighbor))
                if neighbor_tuple not in explored:
                    h = self.manhattan_distance(neighbor, flat_goal, n)
                    heapq.heappush(frontier, (g + 1 + h, neighbor, g + 1, current))
        return None

    @staticmethod
    def print_matrix(matrix):
        # affichage du matrice
        for row in matrix:
            print(" ".join(f"{val:3}" for val in row))
        print()


#-- Programme principal

# if __name__ == "__main__":
#     dimension = int(input("Choisir la dimension (3 ou 4) : "))
#     swap_type = input("Choisir le type de swap (standard, 0-swap, 10-swap) : ").strip().lower()

#     if dimension in {3, 4} and swap_type in {"standard", "0-swap", "10-swap"}:
#         matrices = Matrices()
#         print("\nMatrice initiale :")
#         start_matrix = matrices.current_matrix(dimension)
#         matrices.print_matrix(start_matrix)

#         print("\nMatrice finale :")
#         goal_matrix = matrices.end_matrix(dimension)
#         matrices.print_matrix(goal_matrix)

#         print("\nRésolution du puzzle :")
#         solution = matrices.solve_puzzle(start_matrix, goal_matrix, dimension, swap_type)
#         if solution:
#             print(f"Solution trouvée en {len(solution) - 1} étapes.")
#             for step_num, step in enumerate(solution):
#                 print(f"\nÉtape {step_num + 1} :")
#                 matrices.print_matrix(step)
#         else:
#             print("Aucune solution trouvée.")
#     else:
#         print("Veuillez choisir une dimension valide (3 ou 4) et un type de swap correct (standard, 0-swap, 10-swap).")

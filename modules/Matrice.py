import random
import copy
import heapq

class Matrices:

    #-- Fonction pour le rundom du puzzle
    def current_matrix(self, n):
        values = [i + 1 for i in range(n * n - 1)]
        values.append(0)  
        random.shuffle(values)
        
        matrix = [[0] * n for _ in range(n)]
        index = 0
        for i in range(n):
            for j in range(n):
                matrix[i][j] = values[index]
                index += 1

        for row in matrix:
            print(" ".join(f"{val:3}" for val in row))
        return matrix

    #-- Fonction pour l'etat final du puzzle
    def end_matrix(self, n):
        matrix = [[0] * n for _ in range(n)]
        values = [i + 1 for i in range(n * n - 1)]
        values.append(0) 

        index = 0
        for i in range(n):
            for j in range(n):
                matrix[i][j] = values[index]
                index += 1

        for i in matrix:
            print(" ".join(f"{val:3}" for val in i))
        return matrix

    #-- Fonction pour le calcul du distance de manhattan
    def manhattan_distance(self, etat, goal, n):
        distance = 0
        for i in range(n):
            for j in range(n):
                value = etat[i][j]
                if value != 0:  
                    goal_x, goal_y = next((x, y) for x, row in enumerate(goal) for y, val in enumerate(row) if val == value)
                    # -- Formule du distance de manhattan
                    distance += abs(i - goal_x) + abs(j - goal_y)
        return distance
    
    #--Fonction pour neighbors
    def get_neighbors(self, etat, n):
        neighbors = []

        x, y = next((i, j) for i, line in enumerate(etat) for j, val in enumerate(line) if val == 0)

        # Mouvement de haut , bas, droite, gauche
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n: 
                new_etat = copy.deepcopy(etat)
                new_etat[x][y], new_etat[nx][ny] = new_etat[nx][ny], new_etat[x][y]
                neighbors.append(new_etat)
        return neighbors

    #-- Fonction pour la résolution du puzzle
    def solve_puzzle(self, initial, goal, n):
     
        frontier = []
        heapq.heappush(frontier, (0, initial, 0, None))  

        explored = set()  
        came_from = {} 

        while frontier:
            f, current, g, parent = heapq.heappop(frontier)

            if tuple(map(tuple, current)) in explored:
                continue

            came_from[tuple(map(tuple, current))] = parent
            explored.add(tuple(map(tuple, current)))

            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = came_from[tuple(map(tuple, current))]
                return path[::-1] 

            for neighbor in self.get_neighbors(current, n):
                if tuple(map(tuple, neighbor)) not in explored:
                    h = self.manhattan_distance(neighbor, goal, n)
                    heapq.heappush(frontier, (g + 1 + h, neighbor, g + 1, current))

        return None

#-- progamme test

if __name__ == "__main__":
    dimension = int(input("Choisir la dimension (3 ou 4) : "))
    if dimension in {3, 4}:
        matrices = Matrices()
        print("\nMatrice initiale :")
        start_matrix = matrices.current_matrix(dimension)
        print("\nMatrice finale :")
        goal_matrix = matrices.end_matrix(dimension)
        print("\nRésolution du puzzle :")
        solution = matrices.solve_puzzle(start_matrix, goal_matrix, dimension)
        if solution:
            print(f"Solution trouvée en {len(solution) - 1} étapes.")
            for step_num, step in enumerate(solution):
                print(f"\nÉtape {step_num + 1} :")
                for row in step:
                    print(" ".join(f"{val:3}" for val in row))
        else:
            print("Aucune solution trouvée.")
    else:
        print("Veuillez choisir une dimension valide : 3 ou 4.")

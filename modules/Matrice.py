import random

class Matrices:
    
    def current_matrix(self, n):
        # Créer une liste de valeurs de 1 à (n * n) - 1, et ajouter une case vide (0)
        values = [i + 1 for i in range(n * n - 1)]
        values.append(0) 
       
        random.shuffle(values)
        
        
        matrix = [[0] * n for _ in range(n)] 
        
        
        index = 0  
        for i in range(n):
            for j in range(n):
                matrix[i][j] = values[index]
                index += 1
        

        for i in range(n):
            for j in range(n):
                print("{:3}".format(matrix[i][j]), end=" ")  
            print()  
        
        return matrix

    def end_matrix(self, n):
        
        matrix = [[0] * n for _ in range(n)]
        values = [i + 1 for i in range(n * n - 1)]
        values.append(0)  
        index = 0
        for i in range(n):
            for j in range(n):
                matrix[i][j] = values[index]
                index += 1
        
        
        for i in range(n):
            for j in range(n):
                print("{:3}".format(matrix[i][j]), end=" ")  
            print() 
        
        return matrix

        

dimension = int(input("Choisir la dimension 3 ou 4 : "))

matrices = Matrices()

matrices.current_matrix(dimension)
print("---------------------------")
matrices.end_matrix(dimension)

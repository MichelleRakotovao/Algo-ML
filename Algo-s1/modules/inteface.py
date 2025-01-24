import pygame
import random
import heapq
from modules.sprite import *
from modules.settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.shuffle_time = 0
        self.start_shuffle = False
        self.previous_choice = ""
        self.start_game = False

    def create_game(self):
        grid = [[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
        grid[-1][-1] = 0  # La case vide est en bas à droite
        return grid

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                                                                       self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                                                                       self.tiles_grid[row][col]

    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))


    def manhattan_distance(self, state, goal, n):
        """Calcule la distance de Manhattan entre la grille actuelle et la grille cible."""
        distance = 0
        # Aplatissement de la matrice goal pour recherche facile
        flat_goal = [value for row in goal for value in row]
        for i in range(n):
            for j in range(n):
                value = state[i][j]
                if value != 0:  # Ignore la case vide
                    goal_index = flat_goal.index(value)
                    goal_x, goal_y = divmod(goal_index, n)
                    distance += abs(goal_x - i) + abs(goal_y - j)
        return distance

    def get_neighbors(self, state, n):
        """Génère les voisins possibles en déplaçant la case vide."""
        neighbors = []
        empty_x, empty_y = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in moves:
            x, y = empty_x + dx, empty_y + dy
            if 0 <= x < n and 0 <= y < n:
                new_state = [list(row) for row in state]  # Copie profonde
                new_state[empty_x][empty_y], new_state[x][y] = new_state[x][y], new_state[empty_x][empty_y]
                neighbors.append(new_state)

        return neighbors

    def solve_puzzle(self, initial, goal, n):
        """Résout le puzzle en utilisant A*."""
        frontier = []
        heapq.heappush(frontier, (0, initial, 0, None))  # (coût total, état, coût g, parent)
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
                return path[::-1]  # Retourne le chemin de résolution

            for neighbor in self.get_neighbors(current, n):
                if tuple(map(tuple, neighbor)) not in explored:
                    h = self.manhattan_distance(neighbor, goal, n)
                    heapq.heappush(frontier, (g + 1 + h, neighbor, g + 1, current))

        return None

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.buttons_list = []
        self.buttons_list.append(Button(500, 100, 200, 50, "Shuffle", WHITE, BLACK))
        self.buttons_list.append(Button(500, 170, 200, 50, "Reset", WHITE, BLACK))
        self.buttons_list.append(Button(500, 240, 200, 50, "Solver", WHITE, BLACK))
        self.draw_tiles()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False

        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 120:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True

        self.all_sprites.update()

    def draw_grid(self):
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, GAME_SIZE * TILESIZE))
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE, col))

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            button.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.draw_tiles()

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                        if button.text == "Reset":
                            self.new()
                        if button.text == "Solver":
                            path = self.solve_puzzle(self.tiles_grid, self.tiles_grid_completed, GAME_SIZE)
                            if path:
                                print(f"Solution trouvée en {len(path) - 1} étapes.")
                                for step_num, step in enumerate(path):
                                    print(f"\nÉtape {step_num + 1} :")
                                    for row in step:
                                        print(" ".join(f"{val:3}" for val in row))
                                    self.tiles_grid = step
                                    self.draw_tiles()
                                    self.draw()
                                    pygame.time.delay(300)
                            else:
                                print("Pas de solution trouvée.")

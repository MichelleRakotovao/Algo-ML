import pygame
import sys
import math


# --- Initialisation de Pygame et des Constantes ---
pygame.init()

# Dimensions de l'écran et de la grille
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

BG_COLOR = (10, 25, 47)       # Bleu marine foncé (arrière-plan)
LINE_COLOR = (20, 220, 180)   # Vert néon/fluide pour les lignes
X_COLOR = (255, 255, 255)     # Blanc pur pour le joueur X
O_COLOR = (0, 255, 150)       # Vert fluo pour le joueur O
TEXT_COLOR = (200, 255, 255)  # Cyan pâle pour les textes

# Polices de caractères
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 45)

# Configuration de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Morpion Moderne")

# Variables du jeu
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
current_player = "X"
game_over = False
winner = None
animation_step = 0

# --- Fonctions du Jeu ---

def draw_lines():
    """Dessine les lignes de la grille du morpion."""
    # Lignes horizontales
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), 5)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), 5)
    # Lignes verticales
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), 5)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), 5)

def draw_figures():
    """Dessine les 'X' et les 'O' sur le plateau."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "X":
                x_pos = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y_pos = row * SQUARE_SIZE + SQUARE_SIZE // 2
                # Dessine le 'X' avec une animation simple
                pygame.draw.line(screen, X_COLOR, (x_pos - 50, y_pos - 50), (x_pos + 50, y_pos + 50), LINE_WIDTH)
                pygame.draw.line(screen, X_COLOR, (x_pos + 50, y_pos - 50), (x_pos - 50, y_pos + 50), LINE_WIDTH)
            elif board[row][col] == "O":
                x_pos = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y_pos = row * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.circle(screen, O_COLOR, (x_pos, y_pos), 60, 15)

def mark_square(row, col, player):
    """Marque une case sur le plateau pour le joueur actuel."""
    board[row][col] = player

def available_square(row, col):
    """Vérifie si une case du plateau est disponible."""
    return board[row][col] is None

def is_board_full():
    """Vérifie si le plateau est plein (match nul)."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def check_win(player):
    """Vérifie si le joueur actuel a gagné."""
    # Victoire verticale
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True

    # Victoire horizontale
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    # Victoire diagonale (ascendante)
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        return True

    # Victoire diagonale (descendante)
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player)
        return True

    return False

def draw_vertical_winning_line(col, player):
    """Dessine la ligne de victoire verticale."""
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    color = X_COLOR if player == "X" else O_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), 15)

def draw_horizontal_winning_line(row, player):
    """Dessine la ligne de victoire horizontale."""
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    color = X_COLOR if player == "X" else O_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), 15)

def draw_asc_diagonal(player):
    """Dessine la ligne de victoire diagonale ascendante."""
    color = X_COLOR if player == "X" else O_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)

def draw_desc_diagonal(player):
    """Dessine la ligne de victoire diagonale descendante."""
    color = X_COLOR if player == "X" else O_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)

def restart_game():
    """Réinitialise le jeu à son état initial."""
    global board, current_player, game_over, winner
    board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
    current_player = "X"
    game_over = False
    winner = None
    screen.fill(BG_COLOR)
    draw_lines()

def draw_game_over():
    """Affiche l'écran de fin de partie avec un calque semi-transparent."""

    # Créer un calque semi-transparent pour assombrir l'arrière-plan
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 25, 47, 180))  # Couleur (R, G, B, Alpha) - 180 donne une bonne transparence
    screen.blit(overlay, (0, 0))

    # Afficher le message de victoire ou de match nul
    if winner:
        end_text = font.render(f"{winner} a gagné!", True, TEXT_COLOR)
    else:
        end_text = font.render("Match Nul!", True, TEXT_COLOR)

    text_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(end_text, text_rect)

    # Afficher le message pour recommencer
    restart_text = small_font.render("Appuyez sur 'R' pour Recommencer", True, TEXT_COLOR)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)

# --- Boucle Principale du Jeu ---
draw_lines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, current_player)
                if check_win(current_player):
                    winner = current_player
                    game_over = True
                elif is_board_full():
                    game_over = True

                current_player = "O" if current_player == "X" else "X"
                draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                restart_game()

    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()

    if game_over:
        draw_game_over()

    pygame.display.update()
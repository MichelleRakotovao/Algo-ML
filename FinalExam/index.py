import pygame
import sys
import joblib
import numpy as np

# --- Chargement du modèle IA et des encodeurs ---
clf = joblib.load("tictactoe_model.joblib")
le_board = joblib.load("encoder_board.joblib")
le_move = joblib.load("encoder_move.joblib")


def predict_best_move(board_2d, model, le_board, le_move):
    board_flat = []
    for row in board_2d:
        for cell in row:
            board_flat.append(cell if cell is not None else " ")
    encoded = le_board.transform(board_flat).reshape(1, -1)
    move_encoded = model.predict(encoded)
    move = le_move.inverse_transform(move_encoded)[0]
    i, j = map(int, move.split(","))
    return i, j


# --- Initialisation de Pygame et des Constantes ---
pygame.init()

WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

BG_COLOR = (10, 25, 47)
LINE_COLOR = (20, 220, 180)
X_COLOR = (255, 255, 255)
O_COLOR = (0, 255, 150)
TEXT_COLOR = (200, 255, 255)

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 45)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Morpion IA")

board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
current_player = "X"
game_over = False
winner = None


# --- Fonctions de dessin ---
def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), 5)
    pygame.draw.line(
        screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), 5
    )
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), 5)
    pygame.draw.line(
        screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), 5
    )


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "X":
                x_pos = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y_pos = row * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (x_pos - 50, y_pos - 50),
                    (x_pos + 50, y_pos + 50),
                    LINE_WIDTH,
                )
                pygame.draw.line(
                    screen,
                    X_COLOR,
                    (x_pos + 50, y_pos - 50),
                    (x_pos - 50, y_pos + 50),
                    LINE_WIDTH,
                )
            elif board[row][col] == "O":
                x_pos = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y_pos = row * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.circle(screen, O_COLOR, (x_pos, y_pos), 60, 15)


# --- Fonctions du jeu ---
def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] is None


def is_board_full():
    for row in board:
        for cell in row:
            if cell is None:
                return False
    return True


def check_win(player):
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True
    if board[2][0] == board[1][1] == board[0][2] == player:
        draw_asc_diagonal(player)
        return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        draw_desc_diagonal(player)
        return True
    return False


def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    color = X_COLOR if player == "X" else O_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), 15)


def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    color = X_COLOR if player == "X" else O_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), 15)


def draw_asc_diagonal(player):
    color = X_COLOR if player == "X" else O_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)


def draw_desc_diagonal(player):
    color = X_COLOR if player == "X" else O_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)


def restart_game():
    global board, current_player, game_over, winner
    board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
    current_player = "X"
    game_over = False
    winner = None
    screen.fill(BG_COLOR)
    draw_lines()


def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 25, 47, 180))
    screen.blit(overlay, (0, 0))

    if winner:
        end_text = font.render(f"{winner} a gagné!", True, TEXT_COLOR)
    else:
        end_text = font.render("Match Nul!", True, TEXT_COLOR)

    text_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(end_text, text_rect)

    restart_text = small_font.render(
        "Appuyez sur 'R' pour Recommencer", True, TEXT_COLOR
    )
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)


# --- Boucle principale ---
screen.fill(BG_COLOR)
draw_lines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and not game_over
            and current_player == "X"
        ):
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, "X")
                if check_win("X"):
                    winner = "X"
                    game_over = True
                elif is_board_full():
                    game_over = True
                else:
                    current_player = "O"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_game()

    # Tour de l'IA ("O")
    if current_player == "O" and not game_over:
        pygame.time.wait(500)
        i, j = predict_best_move(board, clf, le_board, le_move)
        if available_square(i, j):
            mark_square(i, j, "O")
            if check_win("O"):
                winner = "O"
                game_over = True
            elif is_board_full():
                game_over = True
            current_player = "X"

    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()

    if game_over:
        draw_game_over()

    pygame.display.update()

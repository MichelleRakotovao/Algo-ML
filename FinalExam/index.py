import pygame
import sys
import joblib
import numpy as np

# Chargement IA
clf = joblib.load("tictactoe_model.joblib")
le_board = joblib.load("encoder_board.joblib")
le_move = joblib.load("encoder_move.joblib")


def predict_best_move(board_2d, model, le_board, le_move):
    board_flat = [
        (cell if cell is not None else " ") for row in board_2d for cell in row
    ]
    encoded = le_board.transform(board_flat).reshape(1, -1)
    move_encoded = model.predict(encoded)
    move = le_move.inverse_transform(move_encoded)[0]
    i, j = map(int, move.split(","))
    return i, j


# Init Pygame
pygame.init()
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 3
LINE_WIDTH = 15
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe IA")

# Couleurs
BG_COLOR = (10, 25, 47)
LINE_COLOR = (20, 220, 180)
X_COLOR = (255, 255, 255)
O_COLOR = (0, 255, 150)
TEXT_COLOR = (200, 255, 255)
BTN_COLOR = (50, 180, 180)
BTN_HOVER = (100, 220, 220)

# Police
font = pygame.font.Font(None, 74)
btn_font = pygame.font.Font(None, 50)

# État du jeu
board = [[None] * 3 for _ in range(3)]
current_player = "X"
game_over = False
winner = None
ia_player = None


def draw_lines():
    for i in range(1, 3):
        pygame.draw.line(
            screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), 5
        )
        pygame.draw.line(
            screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), 5
        )


def draw_figures():
    for row in range(3):
        for col in range(3):
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            if board[row][col] == "X":
                pygame.draw.line(
                    screen, X_COLOR, (x - 50, y - 50), (x + 50, y + 50), LINE_WIDTH
                )
                pygame.draw.line(
                    screen, X_COLOR, (x + 50, y - 50), (x - 50, y + 50), LINE_WIDTH
                )
            elif board[row][col] == "O":
                pygame.draw.circle(screen, O_COLOR, (x, y), 60, 15)


def mark_square(i, j, player):
    board[i][j] = player


def available_square(i, j):
    return board[i][j] is None


def is_board_full():
    return all(board[i][j] is not None for i in range(3) for j in range(3))


def check_win(player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def restart_game():
    global board, current_player, game_over, winner
    board = [[None] * 3 for _ in range(3)]
    current_player = "X"
    game_over = False
    winner = None
    screen.fill(BG_COLOR)
    draw_lines()
    if ia_player == "X":
        pygame.time.wait(500)
        i, j = predict_best_move(board, clf, le_board, le_move)
        mark_square(i, j, "X")
        current_player = "O"


def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 25, 47, 180))
    screen.blit(overlay, (0, 0))
    msg = font.render(
        f"{winner} a gagné!" if winner else "Match nul!", True, TEXT_COLOR
    )
    msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(msg, msg_rect)
    restart = btn_font.render("Appuyez sur R pour recommencer", True, TEXT_COLOR)
    restart_rect = restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart, restart_rect)


def draw_menu():
    screen.fill(BG_COLOR)
    title = font.render("Tic-Tac-Toe IA", True, TEXT_COLOR)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

    btn_x = pygame.Rect(WIDTH // 2 - 150, 200, 300, 80)
    btn_o = pygame.Rect(WIDTH // 2 - 150, 320, 300, 80)

    mx, my = pygame.mouse.get_pos()
    pygame.draw.rect(
        screen, BTN_HOVER if btn_x.collidepoint((mx, my)) else BTN_COLOR, btn_x
    )
    pygame.draw.rect(
        screen, BTN_HOVER if btn_o.collidepoint((mx, my)) else BTN_COLOR, btn_o
    )

    x_text = btn_font.render("IA joue 1 p", True, (0, 0, 0))
    o_text = btn_font.render("IA joue 2 p", True, (0, 0, 0))
    screen.blit(x_text, x_text.get_rect(center=btn_x.center))
    screen.blit(o_text, o_text.get_rect(center=btn_o.center))
    return btn_x, btn_o


def menu_loop():
    global ia_player
    while True:
        btn_x, btn_o = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_x.collidepoint(event.pos):
                    ia_player = "X"
                    return
                elif btn_o.collidepoint(event.pos):
                    ia_player = "O"
                    return
        pygame.display.update()


# Lancer le menu
menu_loop()
restart_game()

# Boucle du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and not game_over
            and current_player != ia_player
        ):
            x, y = event.pos
            row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
            if available_square(row, col):
                mark_square(row, col, current_player)
                if check_win(current_player):
                    winner = current_player
                    game_over = True
                elif is_board_full():
                    game_over = True
                current_player = "O" if current_player == "X" else "X"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_game()

    # Tour IA
    if current_player == ia_player and not game_over:
        pygame.time.wait(500)
        i, j = predict_best_move(board, clf, le_board, le_move)
        if available_square(i, j):
            mark_square(i, j, ia_player)
            if check_win(ia_player):
                winner = ia_player
                game_over = True
            elif is_board_full():
                game_over = True
            current_player = "O" if ia_player == "X" else "X"

    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    if game_over:
        draw_game_over()
    pygame.display.update()

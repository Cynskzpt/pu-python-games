import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 760
LINE_WIDTH = 10
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 12
CROSS_WIDTH = 15
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 50)
BUTTON_ACTIVE = (90, 90, 90)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Fonts
font = pygame.font.SysFont(None, 45)
small_font = pygame.font.SysFont(None, 35)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

player = "X"
game_over = False

# Modes
vs_bot = False

# Buttons
button_2p = pygame.Rect(40, 650, 220, 60)
button_bot = pygame.Rect(340, 650, 220, 60)


def draw_lines():
    """Draw the game board."""
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE),
                     (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE),
                     (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0),
                     (SQUARE_SIZE, WIDTH), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0),
                     (2 * SQUARE_SIZE, WIDTH), LINE_WIDTH)


def draw_figures():
    """Draw X and O symbols."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):

            if board[row][col] == "O":
                pygame.draw.circle(
                    screen,
                    CIRCLE_COLOR,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                     row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    CIRCLE_RADIUS,
                    CIRCLE_WIDTH
                )

            elif board[row][col] == "X":
                pygame.draw.line(
                    screen,
                    CROSS_COLOR,
                    (col * SQUARE_SIZE + SPACE,
                     row * SQUARE_SIZE + SPACE),
                    (col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                     row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                    CROSS_WIDTH
                )

                pygame.draw.line(
                    screen,
                    CROSS_COLOR,
                    (col * SQUARE_SIZE + SPACE,
                     row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                    (col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                     row * SQUARE_SIZE + SPACE),
                    CROSS_WIDTH
                )


def draw_ui():
    """Draw buttons and game status."""
    # Clear bottom area
    pygame.draw.rect(screen, BG_COLOR, (0, WIDTH, WIDTH, HEIGHT - WIDTH))

    # Mode buttons
    pygame.draw.rect(
        screen,
        BUTTON_ACTIVE if not vs_bot else BUTTON_COLOR,
        button_2p,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        BUTTON_ACTIVE if vs_bot else BUTTON_COLOR,
        button_bot,
        border_radius=12
    )

    # Button text
    text_2p = small_font.render("2 Players", True, TEXT_COLOR)
    text_bot = small_font.render("Vs Bot", True, TEXT_COLOR)

    screen.blit(
        text_2p,
        text_2p.get_rect(center=button_2p.center)
    )

    screen.blit(
        text_bot,
        text_bot.get_rect(center=button_bot.center)
    )

    # Game status
    if game_over:
        if check_winner("X"):
            status = "X Wins!"
        elif check_winner("O"):
            status = "O Wins!"
        else:
            status = "Draw!"
    else:
        status = f"{player}'s Turn"

    status_text = font.render(status, True, TEXT_COLOR)
    screen.blit(status_text, (20, 610))

    restart_text = small_font.render("Press R to Restart", True, TEXT_COLOR)
    screen.blit(restart_text, (20, 720))


def mark_square(row, col, symbol):
    board[row][col] = symbol


def available_square(row, col):
    return board[row][col] is None


def is_board_full():
    for row in board:
        if None in row:
            return False
    return True


def check_winner(symbol):
    # Rows
    for row in range(BOARD_ROWS):
        if all(board[row][col] == symbol for col in range(BOARD_COLS)):
            return True

    # Columns
    for col in range(BOARD_COLS):
        if all(board[row][col] == symbol for row in range(BOARD_ROWS)):
            return True

    # Diagonals
    if all(board[i][i] == symbol for i in range(BOARD_ROWS)):
        return True

    if all(board[i][BOARD_ROWS - i - 1] == symbol for i in range(BOARD_ROWS)):
        return True

    return False


def bot_move():
    """Simple random bot."""
    available_moves = []

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if available_square(row, col):
                available_moves.append((row, col))

    if available_moves:
        move = random.choice(available_moves)
        mark_square(move[0], move[1], "O")


def restart():
    global board, player, game_over

    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = "X"
    game_over = False

    screen.fill(BG_COLOR)
    draw_lines()


# Initial setup
screen.fill(BG_COLOR)
draw_lines()

# Main loop
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:

            mouseX, mouseY = event.pos

            # Toggle buttons
            if button_2p.collidepoint(mouseX, mouseY):
                vs_bot = False
                restart()

            elif button_bot.collidepoint(mouseX, mouseY):
                vs_bot = True
                restart()

            # Board clicks
            elif not game_over and mouseY < WIDTH:

                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if available_square(clicked_row, clicked_col):

                    mark_square(clicked_row, clicked_col, player)

                    # Check player win
                    if check_winner(player):
                        game_over = True

                    elif is_board_full():
                        game_over = True

                    else:
                        # Switch player
                        player = "O" if player == "X" else "X"

                        # Bot turn
                        if vs_bot and player == "O" and not game_over:

                            pygame.time.delay(300)

                            bot_move()

                            if check_winner("O"):
                                game_over = True

                            elif is_board_full():
                                game_over = True

                            player = "X"

    # Draw everything
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    draw_ui()

    pygame.display.update()
"""Hangman — browser-sichere Version (gleiche Logik wie Hangman.py)."""
import asyncio
import math
import random

import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" Hangman")

clock = pygame.time.Clock()

BG = (255, 244, 248)
TEXT = (80, 60, 90)
PINK = (255, 182, 193)
DARK_PINK = (255, 120, 170)
WHITE = (255, 255, 255)
MINT = (186, 255, 201)
PURPLE = (180, 150, 255)
RED = (255, 100, 120)


def _font(size: int, bold: bool = False):
    for name in ("arial", "helvetica", "sans"):
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            continue
    return pygame.font.Font(None, size)


font_big = _font(64)
font_med = _font(36)
font_small = _font(28)

words = [
    "strawberry",
    "rainbow",
    "kitten",
    "marshmallow",
    "cupcake",
    "butterfly",
    "sunshine",
    "bubblegum",
    "lavender",
    "penguin",
]

word = random.choice(words).upper()
guessed: list[str] = []
wrong_guesses = 0
max_wrong = 6
game_over = False
win = False

letters: list[list] = []
start_x = 80
start_y = 500
radius = 28
A = 65

for i in range(26):
    x = start_x + (i % 13) * 65
    y = start_y + (i // 13) * 80
    letters.append([x, y, chr(A + i), True])


def draw_background():
    screen.fill(BG)
    for i in range(12):
        x = (i * 90 + pygame.time.get_ticks() * 0.03) % WIDTH
        y = 80 + math.sin(i + pygame.time.get_ticks() * 0.002) * 20
        pygame.draw.circle(screen, WHITE, (int(x), int(y)), 35)


def draw_hangman():
    pygame.draw.line(screen, TEXT, (180, 400), (380, 400), 8)
    pygame.draw.line(screen, TEXT, (280, 400), (280, 120), 8)
    pygame.draw.line(screen, TEXT, (280, 120), (450, 120), 8)
    pygame.draw.line(screen, TEXT, (450, 120), (450, 170), 8)

    if wrong_guesses > 0:
        pygame.draw.circle(screen, PINK, (450, 210), 40)
        pygame.draw.circle(screen, TEXT, (435, 200), 4)
        pygame.draw.circle(screen, TEXT, (465, 200), 4)
        pygame.draw.arc(screen, TEXT, (430, 215, 40, 20), math.pi, 2 * math.pi, 3)

    if wrong_guesses > 1:
        pygame.draw.line(screen, TEXT, (450, 250), (450, 340), 6)
    if wrong_guesses > 2:
        pygame.draw.line(screen, TEXT, (450, 280), (410, 320), 6)
    if wrong_guesses > 3:
        pygame.draw.line(screen, TEXT, (450, 280), (490, 320), 6)
    if wrong_guesses > 4:
        pygame.draw.line(screen, TEXT, (450, 340), (420, 390), 6)
    if wrong_guesses > 5:
        pygame.draw.line(screen, TEXT, (450, 340), (480, 390), 6)


def draw_word():
    display = ""
    for letter in word:
        display += (letter + " ") if letter in guessed else "_ "
    text = font_big.render(display, True, TEXT)
    screen.blit(text, (520, 250))


def draw_letters():
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(screen, MINT, (x, y), radius)
            pygame.draw.circle(screen, DARK_PINK, (x, y), radius, 3)
            text = font_small.render(ltr, True, TEXT)
            screen.blit(
                text,
                (x - text.get_width() // 2, y - text.get_height() // 2),
            )


def check_win():
    return all(letter in guessed for letter in word)


def reset_round():
    global word, guessed, wrong_guesses, game_over, win
    word = random.choice(words).upper()
    guessed = []
    wrong_guesses = 0
    game_over = False
    win = False
    for letter in letters:
        letter[3] = True


async def main():
    global word, guessed, wrong_guesses, game_over, win, letters
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mx, my = event.pos
                for letter in letters:
                    x, y, ltr, visible = letter
                    if not visible:
                        continue
                    if (x - mx) ** 2 + (y - my) ** 2 <= radius * radius:
                        letter[3] = False
                        if ltr not in guessed:
                            guessed.append(ltr)
                        if ltr not in word:
                            wrong_guesses += 1
                        if check_win():
                            win = True
                            game_over = True
                        if wrong_guesses >= max_wrong:
                            game_over = True
                        break

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_over:
                reset_round()

        draw_background()
        title = font_big.render(" Hangman", True, DARK_PINK)
        screen.blit(title, (320, 30))
        draw_hangman()
        draw_word()
        draw_letters()

        if game_over:
            if win:
                msg, color = "You Won!", PURPLE
            else:
                msg, color = f"You Lost! Word: {word}", RED
            screen.blit(font_med.render(msg, True, color), (300, 430))
            screen.blit(
                font_small.render("Press SPACE to play again", True, TEXT),
                (320, 480),
            )

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)


asyncio.run(main())

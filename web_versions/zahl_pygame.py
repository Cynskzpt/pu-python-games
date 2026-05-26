"""Zahl raten — Pygame-Version für den Browser (gleiche Regeln wie Zahl_raten.py)."""
import asyncio
import random

import pygame

pygame.init()

WIDTH, HEIGHT = 520, 420
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zahl raten")

BG = (255, 244, 248)
TEXT = (60, 50, 80)
ACCENT = (0, 245, 212)
WARN = (255, 120, 140)
OK = (120, 200, 140)

font_big = pygame.font.SysFont("comicsansms", 40)
font_med = pygame.font.SysFont("comicsansms", 28)
font_small = pygame.font.SysFont("comicsansms", 22)

geheime_zahl = random.randint(1, 100)
moegliche_versuche = 3
eingabe = ""
message = "Errate die Zahl zwischen 1 und 100"
game_over = False
won = False


def reset_game():
    global geheime_zahl, moegliche_versuche, eingabe, message, game_over, won
    geheime_zahl = random.randint(1, 100)
    moegliche_versuche = 3
    eingabe = ""
    message = "Errate die Zahl zwischen 1 und 100"
    game_over = False
    won = False


def submit_guess():
    global moegliche_versuche, eingabe, message, game_over, won
    if game_over or not eingabe.strip():
        return
    try:
        geratene_zahl = int(eingabe)
    except ValueError:
        message = "Ganz vergessen.. nur ganze Zahlen bitte!"
        moegliche_versuche -= 1
        eingabe = ""
        if moegliche_versuche <= 0:
            game_over = True
            message = f"Leider nicht erraten. Die Zahl war {geheime_zahl}"
        return

    if geratene_zahl > 100:
        message = "Die Zahl liegt doch unter 100!"
        eingabe = ""
        return

    if geratene_zahl > geheime_zahl:
        message = "Zu hoch! Versuch's nochmal!"
        moegliche_versuche -= 1
    elif geratene_zahl < geheime_zahl:
        message = "Zu niedrig! Versuch's nochmal!"
        moegliche_versuche -= 1
    else:
        message = "Richtig geraten!"
        won = True
        game_over = True
        eingabe = ""
        return

    eingabe = ""
    if moegliche_versuche <= 0 and not won:
        game_over = True
        message = f"Leider nicht erraten. Die Zahl war {geheime_zahl}"


async def main():
    global eingabe, game_over
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not game_over:
                    submit_guess()
                elif event.key == pygame.K_BACKSPACE and not game_over:
                    eingabe = eingabe[:-1]
                elif event.key == pygame.K_r and game_over:
                    reset_game()
                elif not game_over:
                    if pygame.K_0 <= event.key <= pygame.K_9 and len(eingabe) < 3:
                        eingabe += chr(event.key)
                    elif event.key == pygame.K_MINUS and not eingabe:
                        eingabe = "-"

        screen.fill(BG)
        title = font_big.render("Zahl raten", True, TEXT)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 24))

        tries = font_med.render(f"Versuche: {moegliche_versuche}", True, TEXT)
        screen.blit(tries, (WIDTH // 2 - tries.get_width() // 2, 80))

        msg_color = OK if won else (WARN if game_over else TEXT)
        msg = font_med.render(message, True, msg_color)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 130))

        box = pygame.Rect(80, 190, WIDTH - 160, 50)
        pygame.draw.rect(screen, (255, 255, 255), box, border_radius=12)
        pygame.draw.rect(screen, ACCENT, box, 3, border_radius=12)
        val = font_big.render(eingabe or "?", True, TEXT)
        screen.blit(val, (box.centerx - val.get_width() // 2, box.centery - val.get_height() // 2))

        hint = font_small.render(
            "Zahl tippen · ENTER · R = neu" if game_over else "Zahl tippen · ENTER zum Prüfen",
            True,
            TEXT,
        )
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 270))

        pygame.display.update()
        await asyncio.sleep(0)


asyncio.run(main())

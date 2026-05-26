"""Lucky Dice — browser-sichere Version (gleiche Logik wie Lucky Dice.py)."""
import asyncio
import random

import pygame

pygame.init()

WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lucky Dice")

clock = pygame.time.Clock()

BG = (20, 24, 35)
CARD = (35, 40, 55)
GREEN = (70, 200, 120)
RED = (220, 80, 80)
WHITE = (240, 240, 240)
GOLD = (255, 215, 100)

title_font = pygame.font.SysFont("arial", 42, bold=True)
font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 22)

money = 100
bet = 10
message = "Press SPACE to roll!"
dice = 1

BTN_PLUS = pygame.Rect(140, 410, 120, 50)
BTN_MINUS = pygame.Rect(290, 410, 120, 50)
BTN_ROLL = pygame.Rect(440, 410, 120, 50)


def draw_text(text, fnt, color, x, y):
    screen.blit(fnt.render(text, True, color), (x, y))


def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)
    draw_text(text, small_font, WHITE, rect.x + 20, rect.y + 12)


def roll_dice():
    return random.randint(1, 6)


def do_roll():
    global money, dice, message
    if money < bet:
        return
    dice = roll_dice()
    if dice >= 4:
        money += bet
        message = "You WON!"
    else:
        money -= bet
        message = "You lost!"


def reset_game():
    global money, bet, message, dice
    money = 100
    bet = 10
    message = "Press SPACE to roll!"
    dice = 1


async def main():
    global money, bet, message, dice
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and money >= bet and money > 0:
                    do_roll()
                elif event.key == pygame.K_r:
                    reset_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if money <= 0 and BTN_ROLL.collidepoint(event.pos):
                    reset_game()
                elif BTN_PLUS.collidepoint(event.pos):
                    bet += 10
                elif BTN_MINUS.collidepoint(event.pos) and bet > 10:
                    bet -= 10
                elif BTN_ROLL.collidepoint(event.pos) and money >= bet and money > 0:
                    do_roll()

        screen.fill(BG)
        draw_text("Lucky Dice", title_font, GOLD, 220, 40)

        pygame.draw.rect(screen, CARD, (150, 120, 400, 250))
        draw_text(f"Dice Roll: {dice}", font, WHITE, 250, 180)
        draw_text(f"Money: ${money}", font, GREEN, 250, 230)
        draw_text(f"Bet: ${bet}", font, WHITE, 250, 280)

        if money <= 0:
            message = "Game Over! Click Roll or press R to restart."
        draw_text(message, small_font, GOLD, 120, 340)

        draw_button("+ Bet", BTN_PLUS, GREEN)
        draw_button("- Bet", BTN_MINUS, RED)
        draw_button("Roll", BTN_ROLL, GOLD)

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)


asyncio.run(main())

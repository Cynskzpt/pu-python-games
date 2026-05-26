import pygame
import random
import sys

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

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=15)
    draw_text(text, small_font, WHITE, x + 20, y + 12)


def roll_dice():
    return random.randint(1, 6)


while True:
    screen.fill(BG)

    
    draw_text("🎲 Lucky Dice 🎲", title_font, GOLD, 180, 40)

    
    pygame.draw.rect(screen, CARD, (150, 120, 400, 250), border_radius=25)

    
    draw_text(f"Dice Roll: {dice}", font, WHITE, 250, 180)

    
    draw_text(f"Money: ${money}", font, GREEN, 250, 230)

    
    draw_text(f"Bet: ${bet}", font, WHITE, 250, 280)

    
    draw_text(message, small_font, GOLD, 180, 340)

    
    draw_button("+ Bet", 140, 410, 120, 50, GREEN)
    draw_button("- Bet", 290, 410, 120, 50, RED)
    draw_button("Roll", 440, 410, 120, 50, GOLD)

    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if money >= bet:
                    dice = roll_dice()

                    
                    if dice >= 4:
                        money += bet
                        message = "You WON!"
                    else:
                        money -= bet
                        message = "You lost!"

    
    if click[0]:
        
        if 140 < mouse[0] < 260 and 410 < mouse[1] < 460:
            bet += 10
            pygame.time.delay(150)

        
        if 290 < mouse[0] < 410 and 410 < mouse[1] < 460:
            if bet > 10:
                bet -= 10
            pygame.time.delay(150)

        
        if 440 < mouse[0] < 560 and 410 < mouse[1] < 460:
            if money >= bet:
                dice = roll_dice()

                if dice >= 4:
                    money += bet
                    message = "You WON!"
                else:
                    money -= bet
                    message = "You lost!"

            pygame.time.delay(150)

    if money <= 0:
        message = "Game Over! Restart to play again."

    pygame.display.update()
    clock.tick(60)
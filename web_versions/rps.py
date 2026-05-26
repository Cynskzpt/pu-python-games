"""Rock Paper Scissors — browser-sichere Version (gleiche Logik wie rock paper scissors2.py)."""
import asyncio
import random

import pygame

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

clock = pygame.time.Clock()

BG = (20, 22, 30)
CARD = (35, 38, 50)
WHITE = (245, 245, 245)
GRAY = (170, 170, 170)
ROCK = (255, 99, 132)
PAPER = (54, 162, 235)
SCISSORS = (255, 206, 86)
GREEN = (80, 200, 120)
RED = (255, 80, 80)

title_font = pygame.font.SysFont("arial", 48, bold=True)
main_font = pygame.font.SysFont("arial", 30)
small_font = pygame.font.SysFont("arial", 22)

choices = ["Rock", "Paper", "Scissors"]
player_choice = ""
computer_choice = ""
result_text = "Choose your move!"
rounds_left = 3
player_score = 0
computer_score = 0
game_over = False


class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        text_surface = main_font.render(self.text, True, WHITE)
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


rock_btn = Button(120, 450, 180, 70, "Rock", ROCK)
paper_btn = Button(360, 450, 180, 70, "Paper", PAPER)
scissors_btn = Button(600, 450, 180, 70, "Scissors", SCISSORS)
buttons = [rock_btn, paper_btn, scissors_btn]


def determine_winner(player, computer):
    global player_score, computer_score
    if player == computer:
        return "Tie Round!"
    if (
        (player == "Rock" and computer == "Scissors")
        or (player == "Paper" and computer == "Rock")
        or (player == "Scissors" and computer == "Paper")
    ):
        player_score += 1
        return "You Win This Round!"
    computer_score += 1
    return "Computer Wins This Round!"


def reset_game():
    global player_choice, computer_choice, result_text
    global rounds_left, player_score, computer_score, game_over
    player_choice = ""
    computer_choice = ""
    result_text = "Choose your move!"
    rounds_left = 3
    player_score = 0
    computer_score = 0
    game_over = False


async def main():
    global player_choice, computer_choice, result_text
    global rounds_left, player_score, computer_score, game_over
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                reset_game()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                for btn in buttons:
                    if btn.clicked(event.pos):
                        player_choice = btn.text
                        computer_choice = random.choice(choices)
                        result_text = determine_winner(player_choice, computer_choice)
                        rounds_left -= 1
                        if rounds_left == 0:
                            game_over = True
                        break

        screen.fill(BG)
        pygame.draw.rect(screen, CARD, (60, 40, 780, 500))

        title = title_font.render("ROCK PAPER SCISSORS", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))

        screen.blit(main_font.render(f"You: {player_score}", True, GREEN), (120, 150))
        screen.blit(main_font.render(f"Computer: {computer_score}", True, RED), (620, 150))
        screen.blit(main_font.render(f"Rounds Left: {rounds_left}", True, WHITE), (350, 150))
        screen.blit(main_font.render(f"Your Choice: {player_choice}", True, WHITE), (120, 240))
        screen.blit(main_font.render(f"Computer Choice: {computer_choice}", True, WHITE), (120, 290))

        result_surface = main_font.render(result_text, True, WHITE)
        screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, 360))

        if not game_over:
            for btn in buttons:
                btn.draw()
        else:
            if player_score > computer_score:
                final_msg, color = "YOU WON THE GAME!", GREEN
            elif player_score < computer_score:
                final_msg, color = "COMPUTER WON!", RED
            else:
                final_msg, color = "IT'S A DRAW!", WHITE
            final_surface = title_font.render(final_msg, True, color)
            screen.blit(final_surface, (WIDTH // 2 - final_surface.get_width() // 2, 430))
            restart_text = small_font.render("Press R to Restart", True, GRAY)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 500))

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)


asyncio.run(main())

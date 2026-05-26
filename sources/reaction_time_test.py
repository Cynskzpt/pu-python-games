import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 950, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reaction Time Challenge")

clock = pygame.time.Clock()

RED = (255, 120, 120)
GREEN = (120, 255, 170)
BLUE = (120, 180, 255)
PURPLE = (200, 170, 255)
TEXT = (50, 50, 70)
WHITE = (255, 255, 255)

font_big = pygame.font.SysFont("comicsansms", 58)
font_med = pygame.font.SysFont("comicsansms", 34)
font_small = pygame.font.SysFont("comicsansms", 26)

state = "waiting"

start_time = 0
wait_time = random.uniform(2, 5)
game_start = time.time()

reaction_times = []
round_number = 1
total_rounds = 5

running = True

def draw_centered(text, font, color, y):
    render = font.render(text, True, color)

    screen.blit(
        render,
        (
            WIDTH // 2 - render.get_width() // 2,
            y
        )
    )

while running:
    clock.tick(60)

    if state == "waiting":
        screen.fill(RED)

        draw_centered(
            f"Round {round_number}/{total_rounds}",
            font_small,
            WHITE,
            120
        )

        draw_centered(
            "Press SPACE when the screen turns green",
            font_small,
            WHITE,
            200
        )

        draw_centered(
            "Wait...",
            font_big,
            WHITE,
            HEIGHT // 2 - 40
        )

        if time.time() - game_start >= wait_time:
            state = "ready"
            start_time = time.time()

    elif state == "ready":
        screen.fill(GREEN)

        draw_centered(
            f"Round {round_number}/{total_rounds}",
            font_small,
            TEXT,
            120
        )

        draw_centered(
            "PRESS SPACE NOW!",
            font_big,
            TEXT,
            HEIGHT // 2 - 40
        )

    elif state == "results":
        screen.fill(PURPLE)

        draw_centered(
            "Reaction Results",
            font_big,
            WHITE,
            40
        )

        table_x = 280
        table_y = 160
        row_height = 60
        col1 = 200
        col2 = 250

        pygame.draw.rect(
            screen,
            WHITE,
            (table_x, table_y, col1 + col2, row_height),
            border_radius=10
        )

        round_text = font_med.render("Round", True, TEXT)
        time_text = font_med.render("Time", True, TEXT)

        screen.blit(round_text, (table_x + 50, table_y + 12))
        screen.blit(time_text, (table_x + 280, table_y + 12))

        for i, reaction in enumerate(reaction_times):
            y = table_y + row_height * (i + 1)

            pygame.draw.rect(
                screen,
                WHITE,
                (table_x, y, col1 + col2, row_height - 5),
                border_radius=10
            )

            round_label = font_small.render(
                f"{i + 1}",
                True,
                TEXT
            )

            reaction_label = font_small.render(
                f"{reaction} ms",
                True,
                TEXT
            )

            screen.blit(round_label, (table_x + 80, y + 14))
            screen.blit(reaction_label, (table_x + 250, y + 14))

        average = int(sum(reaction_times) / len(reaction_times))

        draw_centered(
            f"Average: {average} ms",
            font_med,
            WHITE,
            540
        )

        draw_centered(
            "Press R to play again",
            font_small,
            WHITE,
            590
        )

    elif state == "early":
        screen.fill(BLUE)

        draw_centered(
            "Too Early!",
            font_big,
            WHITE,
            HEIGHT // 2 - 50
        )

        draw_centered(
            "Press R to restart",
            font_small,
            WHITE,
            HEIGHT // 2 + 40
        )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                if state == "waiting":
                    state = "early"

                elif state == "ready":
                    reaction = int(
                        (time.time() - start_time) * 1000
                    )

                    reaction_times.append(reaction)

                    if round_number >= total_rounds:
                        state = "results"
                    else:
                        round_number += 1
                        state = "waiting"
                        wait_time = random.uniform(2, 5)
                        game_start = time.time()

            if event.key == pygame.K_r:
                if state in ["results", "early"]:
                    reaction_times = []
                    round_number = 1
                    state = "waiting"
                    wait_time = random.uniform(2, 5)
                    game_start = time.time()

    pygame.display.update()

pygame.quit()
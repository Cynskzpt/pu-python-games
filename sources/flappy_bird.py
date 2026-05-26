import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" Flappy Bird")

clock = pygame.time.Clock()
FPS = 60

SKY = (196, 235, 255)
GROUND = (181, 234, 165)
PIPE = (125, 204, 144)
PIPE_DARK = (90, 170, 110)
BIRD = (255, 221, 120)
BIRD_WING = (255, 193, 90)
WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
PINK = (255, 183, 197)

font = pygame.font.SysFont("comicsansms", 42)
small_font = pygame.font.SysFont("comicsansms", 24)

gravity = 0.45
bird_movement = 0
score = 0
best_score = 0
game_active = True

bird_x = 120
bird_y = HEIGHT // 2
bird_radius = 20

pipe_width = 90
pipe_gap = 190
pipe_speed = 4

clouds = []

for _ in range(6):
    clouds.append([
        random.randint(0, WIDTH),
        random.randint(50, HEIGHT - 200),
        random.randint(50, 100)
    ])

pipes = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1400)

def create_pipe():
    height = random.randint(180, 500)
    top_pipe = pygame.Rect(WIDTH + 50, 0, pipe_width, height - pipe_gap // 2)
    bottom_pipe = pygame.Rect(WIDTH + 50, height + pipe_gap // 2, pipe_width, HEIGHT)
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return [pipe for pipe in pipes if pipe.right > -50]

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, PIPE, pipe, border_radius=16)
        pygame.draw.rect(screen, PIPE_DARK, pipe.inflate(-18, 0), border_radius=12)

        if pipe.top <= 0:
            cap = pygame.Rect(pipe.x - 8, pipe.bottom - 25, pipe_width + 16, 25)
        else:
            cap = pygame.Rect(pipe.x - 8, pipe.y, pipe_width + 16, 25)

        pygame.draw.rect(screen, PIPE_DARK, cap, border_radius=12)

def check_collision(pipes):
    bird_rect = pygame.Rect(
        bird_x - bird_radius,
        bird_y - bird_radius,
        bird_radius * 2,
        bird_radius * 2
    )

    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_y <= 0 or bird_y >= HEIGHT - 90:
        return False

    return True

def draw_bird(y, flap):
    bob = math.sin(flap * 0.2) * 2

    pygame.draw.circle(screen, BIRD, (bird_x, int(y + bob)), bird_radius)

    wing_y = y + math.sin(flap * 0.5) * 6
    pygame.draw.ellipse(
        screen,
        BIRD_WING,
        (bird_x - 8, wing_y, 24, 14)
    )

    pygame.draw.circle(screen, WHITE, (bird_x + 8, int(y - 5)), 7)
    pygame.draw.circle(screen, BLACK, (bird_x + 10, int(y - 4)), 3)

    beak = [
        (bird_x + 18, y + 2),
        (bird_x + 32, y + 7),
        (bird_x + 18, y + 12)
    ]
    pygame.draw.polygon(screen, PINK, beak)

    blush1 = (bird_x - 2, y + 10)
    blush2 = (bird_x + 10, y + 12)

    pygame.draw.circle(screen, PINK, blush1, 4)
    pygame.draw.circle(screen, PINK, blush2, 4)

def draw_clouds():
    for cloud in clouds:
        cloud[0] -= 0.3

        if cloud[0] < -120:
            cloud[0] = WIDTH + 50
            cloud[1] = random.randint(50, HEIGHT - 200)

        x, y, size = cloud

        pygame.draw.circle(screen, WHITE, (int(x), int(y)), size // 2)
        pygame.draw.circle(screen, WHITE, (int(x + size // 2), int(y)), size // 2)
        pygame.draw.circle(screen, WHITE, (int(x + size // 4), int(y - size // 3)), size // 2)

def draw_ground():
    pygame.draw.rect(screen, GROUND, (0, HEIGHT - 90, WIDTH, 90))

    for i in range(0, WIDTH, 40):
        pygame.draw.arc(
            screen,
            (150, 210, 130),
            (i, HEIGHT - 75, 40, 30),
            0,
            math.pi,
            3
        )

def display_score():
    score_surface = font.render(str(score), True, BLACK)
    score_rect = score_surface.get_rect(center=(WIDTH // 2, 80))
    screen.blit(score_surface, score_rect)

def game_over_screen():
    title = font.render(" Flappy", True, BLACK)
    tip = small_font.render("Press SPACE to play again", True, BLACK)
    best = small_font.render(f"Best Score: {best_score}", True, BLACK)

    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
    screen.blit(tip, tip.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    screen.blit(best, best.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))

running = True
flap_timer = 0

while running:
    clock.tick(FPS)
    flap_timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -8

            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipes.clear()
                bird_y = HEIGHT // 2
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE and game_active:
            pipes.extend(create_pipe())

    screen.fill(SKY)

    draw_clouds()

    if game_active:
        bird_movement += gravity
        bird_y += bird_movement

        pipes = move_pipes(pipes)
        draw_pipes(pipes)

        draw_bird(bird_y, flap_timer)

        game_active = check_collision(pipes)

        for pipe in pipes:
            if pipe.centerx == bird_x:
                score += 0.5

        score = int(score)
        best_score = max(best_score, score)

        display_score()

    else:
        draw_bird(bird_y, flap_timer)
        game_over_screen()

    draw_ground()

    pygame.display.update()

pygame.quit()
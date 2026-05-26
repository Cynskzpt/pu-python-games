import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 360
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pac-Man")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 105, 180)
WHITE = (255, 255, 255)

TILE = 40

# ORIGINAL STYLE MAP (restored)
maze = [
    "####################",
    "#........##........#",
    "#.####.#.##.#.####.#",
    "#..................#",
    "#.####.######.####.#",
    "#..................#",
    "#.####.#.##.#.####.#",
    "#........##........#",
    "####################"
]

# Player
player_x = TILE
player_y = TILE
speed = TILE

# Ghosts (simple movement)
ghosts = [
    {"x": 10*TILE, "y": 3*TILE, "dx": TILE, "dy": 0, "color": RED},
    {"x": 8*TILE, "y": 5*TILE, "dx": -TILE, "dy": 0, "color": PINK},
]

# Dots
dots = []

for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == ".":
            dots.append(pygame.Rect(x*TILE+15, y*TILE+15, 10, 10))


def draw_maze():
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == "#":
                pygame.draw.rect(screen, BLUE, (x*TILE, y*TILE, TILE, TILE))


def draw_dots():
    for d in dots:
        pygame.draw.rect(screen, WHITE, d)


def move_player(dx, dy):
    global player_x, player_y

    new_x = player_x + dx
    new_y = player_y + dy

    grid_x = new_x // TILE
    grid_y = new_y // TILE

    if maze[grid_y][grid_x] != "#":
        player_x = new_x
        player_y = new_y


def move_ghosts():
    for g in ghosts:
        new_x = g["x"] + g["dx"]
        new_y = g["y"] + g["dy"]

        grid_x = new_x // TILE
        grid_y = new_y // TILE

        if maze[grid_y][grid_x] == "#":
            g["dx"] *= -1
            g["dy"] *= -1
        else:
            g["x"] = new_x
            g["y"] = new_y


def draw_player():
    pygame.draw.circle(screen, YELLOW,
                       (player_x + TILE//2, player_y + TILE//2),
                       TILE//2 - 3)


def draw_ghosts():
    for g in ghosts:
        pygame.draw.rect(screen, g["color"],
                         (g["x"], g["y"], TILE, TILE))


score = 0
font = pygame.font.SysFont("Arial", 24)

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        move_player(-speed, 0)
    if keys[pygame.K_RIGHT]:
        move_player(speed, 0)
    if keys[pygame.K_UP]:
        move_player(0, -speed)
    if keys[pygame.K_DOWN]:
        move_player(0, speed)

    move_ghosts()

    # Eat dots
    p_rect = pygame.Rect(player_x, player_y, TILE, TILE)
    for d in dots[:]:
        if p_rect.colliderect(d):
            dots.remove(d)
            score += 1

    # Ghost collision = game over
    for g in ghosts:
        g_rect = pygame.Rect(g["x"], g["y"], TILE, TILE)
        if p_rect.colliderect(g_rect):
            print("GAME OVER")
            pygame.quit()
            sys.exit()

    # Draw
    draw_maze()
    draw_dots()
    draw_player()
    draw_ghosts()

    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, HEIGHT - 30))

    pygame.display.flip()
    clock.tick(8)

pygame.quit()
sys.exit()
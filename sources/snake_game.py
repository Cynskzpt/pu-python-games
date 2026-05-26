import pygame
import random

pygame.init()
# Game constants
WIDTH, HEIGHT = 640, 480
BLOCK_SIZE = 20
SPEED = 7

# Colors
BLUE = (0, 153, 255)
ORANGE = (0, 204, 102)
YELLLOW = (255, 255, 153)

# Initialize game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Snake class
class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (1, 0)

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0] * BLOCK_SIZE, head[1] + self.direction[1] * BLOCK_SIZE)
        self.body.insert(0, new_head)

    def eat(self, food):
        if self.body[0] == food:
            return True
        else:
            self.body.pop()
            return False

    def draw(self):
        for pos in self.body:
            rect = (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen , ORANGE, rect )

# Food class
class Food:
    def __init__(self):
        random_x = random.randint(0, WIDTH - BLOCK_SIZE)
        random_y = random.randint(0, HEIGHT - BLOCK_SIZE)
        self.pos = (random_x // BLOCK_SIZE * BLOCK_SIZE , random_y // BLOCK_SIZE * BLOCK_SIZE)

    def draw(self):
        pygame.draw.rect(screen, YELLLOW, (self.pos[0], self.pos[1], BLOCK_SIZE, BLOCK_SIZE))


def start_game():
    # Game loop
    snake = Snake()
    food = Food()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP :
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.direction = (1, 0)

        snake.move()
        if snake.eat(food.pos):
            food = Food()
        else:
            if (snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH or
                snake.body[0][1] < 0 or snake.body[0][1] >= HEIGHT):
                running = False

        screen.fill(BLUE)
        snake.draw()
        food.draw()
        pygame.display.flip()
        clock.tick(SPEED)

    #pygame.quit()

start_game()
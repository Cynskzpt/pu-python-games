import pygame
import random

# Inicialización de Pygame
pygame.init()

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
colors = [
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (0, 255, 0),  # Green
    (128, 0, 128),  # Purple
    (255, 0, 0)  # Red
]

# Dimensiones del tablero
width, height = 300, 600
block_size = 30
cols = width // block_size
rows = height // block_size

# Crear ventana
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tetris')

# Fuente para el puntaje y mensaje de pérdida
font = pygame.font.SysFont('comicsans', 30)

# Figuras y sus rotaciones (corregido como listas de listas de listas)
shapes = [
    [['.....', '.....', '..00.', '.00..', '.....'],  # S
     ['.....', '..0..', '..00.', '...0.', '.....']],

    [['.....', '.....', '.00..', '..00.', '.....'],  # Z
     ['.....', '..0..', '.00..', '.0...', '.....']],

    [['.....', '..0..', '.000.', '.....', '.....'],  # T
     ['.....', '..0..', '..00.', '..0..', '.....'],
     ['.....', '.....', '.000.', '..0..', '.....'],
     ['.....', '..0..', '.00..', '..0..', '.....']],

    [['.....', '.0...', '.000.', '.....', '.....'],  # L
     ['.....', '..00.', '..0..', '..0..', '.....'],
     ['.....', '.....', '.000.', '...0.', '.....'],
     ['.....', '..0..', '..0..', '.00..', '.....']],

    [['.....', '...0.', '.000.', '.....', '.....'],  # J
     ['.....', '..0..', '..0..', '..00.', '.....'],
     ['.....', '.....', '.000.', '.0...', '.....'],
     ['.....', '.00..', '..0..', '..0..', '.....']],

    [['.....', '.....', '.00..', '.00..', '.....']],  # O

    [['..0..', '..0..', '..0..', '..0..', '.....'],  # I
     ['.....', '0000.', '.....', '.....', '.....']]
]


# Clase para definir las piezas
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(colors)
        self.rotation = 0

    # Devolver la rotación actual de la pieza
    def image(self):
        return self.shape[self.rotation % len(self.shape)]

    def rotate(self):
        self.rotation += 1


# Crear el tablero vacío
def create_grid(locked_positions={}):
    grid = [[black for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid


# Dibuja la cuadrícula
def draw_grid(grid):
    for i in range(rows):
        for j in range(cols):
            pygame.draw.rect(screen, grid[i][j], (j * block_size, i * block_size, block_size, block_size), 0)

    for i in range(rows):
        pygame.draw.line(screen, gray, (0, i * block_size), (width, i * block_size))  # Líneas horizontales
    for j in range(cols):
        pygame.draw.line(screen, gray, (j * block_size, 0), (j * block_size, height))  # Líneas verticales


# Función para dibujar el puntaje en la pantalla
def draw_score(score):
    label = font.render(f'Score: {score}', True, white)
    screen.blit(label, (10, 10))  # Mostrar en la esquina superior izquierda


# Función para mostrar el mensaje de pérdida
def draw_lost_message():
    label = font.render('You lost!', True, white)
    screen.blit(label, (width // 2 - label.get_width() // 2, height // 2 - label.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(1500)


# Verifica si la posición es válida
def valid_space(piece, grid):
    formatted = convert_shape_format(piece)

    for pos in formatted:
        x, y = pos
        if y >= rows or x < 0 or x >= cols or y >= 0 and grid[y][x] != black:
            return False
    return True


# Convertir la pieza en una lista de celdas para dibujarla
def convert_shape_format(piece):
    positions = []
    shape_format = piece.image()

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    return positions


# Colocar las piezas en posiciones bloqueadas cuando tocan el fondo o piezas anteriores
def lock_positions(piece, grid, locked_positions):
    formatted = convert_shape_format(piece)
    for pos in formatted:
        locked_positions[(pos[0], pos[1])] = piece.color


# Eliminar filas completas y sumar puntos
def clear_rows(grid, locked_positions):
    increment = 0
    for i in range(rows - 1, -1, -1):
        row = grid[i]
        if black not in row:
            increment += 1
            ind = i
            for j in range(cols):
                try:
                    del locked_positions[(j, i)]
                except:
                    continue

    if increment > 0:
        for key in sorted(list(locked_positions), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + increment)
                locked_positions[new_key] = locked_positions.pop(key)

    return increment


# Función principal del juego
def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = Piece(cols // 2 - 1, 0, random.choice(shapes))
    next_piece = Piece(cols // 2 - 1, 0, random.choice(shapes))
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.3
        fall_time += clock.get_rawtime()
        clock.tick()

        # Caída automática de la pieza
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        piece_pos = convert_shape_format(current_piece)
        for pos in piece_pos:
            x, y = pos
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece:
            lock_positions(current_piece, grid, locked_positions)
            current_piece = next_piece
            next_piece = Piece(cols // 2 - 1, 0, random.choice(shapes))
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_grid(grid)
        draw_score(score)  # Dibuja el puntaje en la pantalla
        pygame.display.update()

        if any(y <= 1 for _, y in locked_positions):
            draw_lost_message()  # Muestra el mensaje de "Perdiste"
            run = False  # Termina el juego

    pygame.quit()


if __name__ == "__main__":
    main()
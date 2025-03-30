import pygame
import numpy as np

# Configurações do grid
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 8
RADIUS_SIZE = 1
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
FPS = 15

# Cores
BACKGROUND_COLOR = (0, 0, 0)
CELL_COLOR = (255, 255, 255)

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Criar a grade do autômato celular
grid = np.zeros((ROWS, COLS), dtype=int)

def draw_grid():
    screen.fill(BACKGROUND_COLOR)
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row, col] == 1:
                pygame.draw.rect(screen, CELL_COLOR, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

def update_grid():
    global grid
    new_grid = np.copy(grid)
    for row in range(ROWS):
        for col in range(COLS):
            # Contar células vizinhas vivas
            neighbors = np.sum(grid[max(0, row - 1):min(ROWS, row + 2), max(0, col - 1):min(COLS, col + 2)]) - grid[row, col]
            
            # Aplicar regras do Jogo da Vida
            if grid[row, col] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[row, col] = 0  # Morte por solidão ou superpopulação
            elif grid[row, col] == 0 and neighbors == 3:
                new_grid[row, col] = 1  # Reprodução
    grid = new_grid

def add_cells_with_neighbors(x, y, radius=RADIUS_SIZE):
    """Adiciona células no ponto clicado e em seus arredores"""
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    
    for i in range(-radius, radius+1):
        for j in range(-radius, radius+1):
            new_row, new_col = row + i, col + j
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                grid[new_row, new_col] = 1

def main():
    running = True
    drawing = False  # Flag para controlar quando está desenhando
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    add_cells_with_neighbors(event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    add_cells_with_neighbors(event.pos[0], event.pos[1])
        
        update_grid()
        
        draw_grid()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
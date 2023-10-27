import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

# Couleurs
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Couleurs des pièces
PIECE_COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 165, 0)  # Orange
]

# Initialisation de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Classe TetrisGrid
class TetrisGrid:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    def is_occupied(self, x, y):
        return self.grid[y][x] != 0

    def lock_piece(self, piece):
        for x, y in piece.get_occupied_cells():
            self.grid[y][x] = piece.color

    def check_lines(self):
        lines_cleared = 0
        for y in range(GRID_HEIGHT - 1, -1, -1):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0] * GRID_WIDTH)
                lines_cleared += 1
        return lines_cleared

# Classe TetrisPiece
class TetrisPiece:
    SHAPES = [
        [[1, 1, 1, 1]],
        [[1, 1], [1, 1]],
        [[1, 1, 1], [0, 1, 0]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 1, 1], [0, 0, 1]],
        [[1, 1, 1], [0, 1, 0]],
        [[1, 1, 1], [1, 0, 0]]
    ]

    def __init__(self, shape, x, y):
        self.shape = shape
        self.x = x
        self.y = y
        self.rotation = 0
        self.color = random.choice(PIECE_COLORS)

    def get_occupied_cells(self):
        cells = []
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    cells.append((self.x + j, self.y + i))
        return cells

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)
        self.shape = self.SHAPES[self.rotation]

# Fonction pour dessiner la grille
def draw_grid(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] != 0:
                pygame.draw.rect(screen, grid[y][x], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Fonction pour dessiner la pièce
def draw_piece(piece):
    for x, y in piece.get_occupied_cells():
        pygame.draw.rect(screen, piece.color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Fonction pour dessiner les pièces à venir
def draw_next_pieces(next_pieces):
    next_x = WIDTH + 20
    next_y = 50

    for piece in next_pieces:
        for i in range(len(piece.shape)):
            for j in range(len(piece.shape[0])):
                if piece.shape[i][j]:
                    pygame.draw.rect(screen, piece.color, (next_x + j * CELL_SIZE, next_y + i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Générer les pièces à venir
def generate_next_pieces(num_pieces):
    next_pieces = [TetrisPiece(random.choice(TetrisPiece.SHAPES), 0, 0) for _ in range(num_pieces)]
    return next_pieces

# Mettre à jour l'état du jeu ici
def update_game_state(score, grid, current_piece, next_pieces):
    # Vérifier s'il y a une collision
    if not can_move(current_piece, 0, 1, grid):
        # Collision avec la grille du bas
        grid.lock_piece(current_piece)
        lines_cleared = grid.check_lines()
        score += lines_cleared * 100
        # Générer une nouvelle pièce
        current_piece = next_pieces.pop(0)
        next_pieces.append(TetrisPiece(random.choice(TetrisPiece.SHAPES), GRID_WIDTH // 2 - 1, 0))
    else:
        # Déplacer la pièce vers le bas
        current_piece.y += 1

    return score, current_piece

# Fonction pour vérifier si la pièce peut se déplacer
def can_move(piece, dx, dy, grid):
    for x, y in piece.get_occupied_cells():
        new_x, new_y = x + dx, y + dy
        if (
            new_x < 0
            or new_x >= GRID_WIDTH
            or new_y >= GRID_HEIGHT
            or (new_y >= 0 and grid.is_occupied(new_x, new_y))
        ):
            return False
    return True

# Boucle principale
def main():
    clock = pygame.time.Clock()
    grid = TetrisGrid()
    current_piece = TetrisPiece(random.choice(TetrisPiece.SHAPES), GRID_WIDTH // 2 - 1, 0)
    next_pieces = generate_next_pieces(3)
    score = 0

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if can_move(current_piece, -1, 0, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if can_move(current_piece, 1, 0, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_DOWN:
                    if can_move(current_piece, 0, 1, grid):
                        current_piece.y += 1
                elif event.key == pygame.K_UP:
                    rotated_piece = TetrisPiece(current_piece.shape, current_piece.x, current_piece.y)
                    rotated_piece.rotate()
                    if can_move(rotated_piece, 0, 0, grid):
                        current_piece.rotate()

        # Mettre à jour l'état du jeu
        score, current_piece = update_game_state(score, grid, current_piece, next_pieces)

        screen.fill((0, 0, 0))
        draw_grid(grid.grid)
        draw_piece(current_piece)
        draw_next_pieces(next_pieces)

        # Mettre à jour l'affichage
        pygame.display.flip()
        clock.tick(5)  # Contrôle de la vitesse du jeu

    pygame.quit()
    exit()

if __name__ == '__main__':
    main()

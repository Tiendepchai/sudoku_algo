import pygame
import sys
import random
from pygame.locals import *
from grid import grid  # assuming you have the grid class in grid.py

# Initialize pygame
pygame.init()

# Set screen dimensions and variables
WIDTH, HEIGHT = 540, 600  # 9x9 grid and some extra space at the bottom
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

# Create a grid object
sudoku_grid = grid()

# Selected cell
selected = None
grid_size = WIDTH // 9

def draw_grid():
    # Draw 9x9 grid lines
    for i in range(10):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (i * grid_size, 0), (i * grid_size, WIDTH), 4)
            pygame.draw.line(screen, BLACK, (0, i * grid_size), (WIDTH, i * grid_size), 4)
        else:
            pygame.draw.line(screen, GREY, (i * grid_size, 0), (i * grid_size, WIDTH), 2)
            pygame.draw.line(screen, GREY, (0, i * grid_size), (WIDTH, i * grid_size), 2)

def draw_numbers():
    # Draw the numbers in the grid
    for i in range(9):
        for j in range(9):
            if sudoku_grid.matrix[i][j] != 0:
                text = font.render(str(sudoku_grid.matrix[i][j]), True, BLACK)
                screen.blit(text, (j * grid_size + 20, i * grid_size + 10))

def draw_selected():
    # Highlight the selected cell
    if selected:
        row, col = selected
        pygame.draw.rect(screen, BLUE, (col * grid_size, row * grid_size, grid_size, grid_size), 4)

def handle_click(pos):
    # Convert the mouse click position into a grid index
    global selected
    x, y = pos
    if x < WIDTH and y < WIDTH:  # Ensure click is inside the grid
        selected = (y // grid_size, x // grid_size)

def handle_input(key):
    # Handle number input from the user
    if selected:
        row, col = selected
        if key == K_1:
            sudoku_grid.matrix[row][col] = 1
        elif key == K_2:
            sudoku_grid.matrix[row][col] = 2
        elif key == K_3:
            sudoku_grid.matrix[row][col] = 3
        elif key == K_4:
            sudoku_grid.matrix[row][col] = 4
        elif key == K_5:
            sudoku_grid.matrix[row][col] = 5
        elif key == K_6:
            sudoku_grid.matrix[row][col] = 6
        elif key == K_7:
            sudoku_grid.matrix[row][col] = 7
        elif key == K_8:
            sudoku_grid.matrix[row][col] = 8
        elif key == K_9:
            sudoku_grid.matrix[row][col] = 9
        elif key == K_BACKSPACE or key == K_DELETE:
            sudoku_grid.matrix[row][col] = 0

def solve_puzzle():
    sudoku_grid.solve_sudoku()

def generate_valid_sudoku():  
  sudoku_grid.reset_board()
  sudoku_grid.fillValues()



def generateCont(self): # uses recursion to finish generating a random board
    
    return False
def draw_start_button():
    button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 50, 140, 40)
    pygame.draw.rect(screen, GREEN, button_rect)
    text = small_font.render("Start", True, WHITE)
    screen.blit(text, (WIDTH - 130, HEIGHT - 45))
    return button_rect

def main():
    global selected
    running = True
    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_numbers()
        draw_selected()

        # Draw the Start button
        start_button = draw_start_button()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if start_button.collidepoint(event.pos):
                        generate_valid_sudoku()  # Generate a starting point
                    else:
                        handle_click(event.pos)

            if event.type == KEYDOWN:
                handle_input(event.key)

            # Solve sudoku when pressing space
            if event.type == KEYDOWN and event.key == K_SPACE:
                solve_puzzle()

        pygame.display.update()

if __name__ == "__main__":
    main()

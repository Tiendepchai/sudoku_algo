import pygame
import sys
from pygame.locals import *
from grid import *  # assuming you have the grid class in grid.py

# Initialize pygame
pygame.init()

# Set screen dimensions and variables
WIDTH, HEIGHT = 540, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255,0,0)
# Fonts
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

# Create a grid object
sudoku_grid = grid()

# Selected cell and grid size
selected = None
grid_size = WIDTH // 9

# Game state
menu = 1  # Start with menu screen

def draw_grid():
    for i in range(10):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (i * grid_size, 0), (i * grid_size, WIDTH), 4)
            pygame.draw.line(screen, BLACK, (0, i * grid_size), (WIDTH, i * grid_size), 4)
        else:
            pygame.draw.line(screen, GREY, (i * grid_size, 0), (i * grid_size, WIDTH), 2)
            pygame.draw.line(screen, GREY, (0, i * grid_size), (WIDTH, i * grid_size), 2)

def draw_numbers(player=False):
    for i in range(9):
        for j in range(9):
            # Check if the cell is a preset (initial) number
            if sudoku_grid.matrix[i][j] != 0:
                # Render preset numbers in black
                text = font.render(str(sudoku_grid.matrix[i][j]), True, BLACK)
                screen.blit(text, (j * grid_size + 20, i * grid_size + 10))
            elif player and sudoku_grid.user[i][j] != 0 and sudoku_grid.user[i][j]:
                # Render user input: red if incorrect, black if correct
                color = BLACK if sudoku_grid.matrix[i][j] == sudoku_grid.user[i][j] else RED
                text = font.render(str(sudoku_grid.user[i][j]), True, color)
                screen.blit(text, (j * grid_size + 20, i * grid_size + 10))


def draw_selected():
    if selected:
        row, col = selected
        pygame.draw.rect(screen, BLUE, (col * grid_size, row * grid_size, grid_size, grid_size), 4)

def handle_click(pos):
    global selected
    x, y = pos
    if x < WIDTH and y < WIDTH:
        selected = (y // grid_size, x // grid_size)

def handle_input(key, player = False):
    if selected and not player:
        row, col = selected
        if key in range(K_1, K_9 + 1):
            sudoku_grid.matrix[row][col] = key - K_0
        elif key == K_BACKSPACE or key == K_DELETE:
            sudoku_grid.matrix[row][col] = 0
    else: 
        row, col = selected
        if key in range(K_1, K_9 + 1):
            sudoku_grid.user[row][col] = key - K_0

        elif key == K_BACKSPACE or key == K_DELETE:
            sudoku_grid.user[row][col] = 0

def solve_puzzle():
    sudoku_grid.solve_sudoku()

def generate_valid_sudoku():
    sudoku_grid.reset_board()
    sudoku_grid.fillValues()

def draw_start_button():
    button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 50, 140, 40)
    pygame.draw.rect(screen, GREEN, button_rect)
    text = small_font.render("START", True, WHITE)
    screen.blit(text, (WIDTH - 130, HEIGHT - 45))
    return button_rect

def draw_clear_button():
    button_rect = pygame.Rect(10, HEIGHT - 50, 140, 40)  # Positioned to the left
    pygame.draw.rect(screen, GREEN, button_rect)
    text = small_font.render("CLEAR", True, WHITE)
    screen.blit(text, (30, HEIGHT - 45))  # Adjust text position within the button
    return button_rect


def draw_menu():
    screen.fill(WHITE)
    title = font.render("Sudoku Menu", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 150))

    # Play Sudoku button
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    pygame.draw.rect(screen, BLUE, play_button)
    play_text = small_font.render("Play Sudoku", True, WHITE)
    screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 - 40))

    # Sudoku solver button
    solver_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, GREEN, solver_button)
    generate_text = small_font.render("Sudoku Solver", True, WHITE)
    screen.blit(generate_text, (WIDTH // 2 - generate_text.get_width() // 2, HEIGHT // 2 + 60))

    return  solver_button, play_button

def main():
    global selected, menu
    running = True
    while running:
        if menu == 1:
            # Display menu
            solver_button, play_button = draw_menu()
        elif menu == 2:
            # Display main solver
            screen.fill(WHITE)
            draw_grid()
            draw_numbers()
            draw_selected()
            clear_button = draw_clear_button()

        else:
            # Display main game
            screen.fill(WHITE)
            draw_grid()
            draw_numbers(player=True)
            draw_selected()
            clear_button = draw_clear_button()
            start_button = draw_start_button()


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if menu == 1:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if solver_button.collidepoint(event.pos):
                        menu = 2 
                        
                    elif play_button.collidepoint(event.pos):
                        menu = 3  
                        generate_valid_sudoku()
                    
            elif menu == 3:
                if event.type == MOUSEBUTTONDOWN:
                    if clear_button.collidepoint(event.pos):
                        sudoku_grid.reset_board()
                    else:
                        handle_click(event.pos)

                if event.type == MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        generate_valid_sudoku()
                    else:
                        handle_click(event.pos) 

                if event.type == KEYDOWN:
                    handle_input(event.key, player=True)

            elif menu == 2:
                if event.type == MOUSEBUTTONDOWN:
                    if clear_button.collidepoint(event.pos):
                        sudoku_grid.reset_board()
                    else:
                        handle_click(event.pos)

                

                if event.type == KEYDOWN:
                    handle_input(event.key)

                if event.type == KEYDOWN and event.key == K_SPACE and menu != 3:
                    solve_puzzle()

        pygame.display.update()

if __name__ == "__main__":
    main()

import pygame

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 50
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
UI_HEIGHT = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT + UI_HEIGHT))
pygame.display.set_caption("Grid Snap")

clock = pygame.time.Clock()

# Create grid cells
grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Create UI elements
ui_elements = [
    (RED, pygame.Rect(10, HEIGHT + 10, 50, 30)),   # Red box
    (GREEN, pygame.Rect(70, HEIGHT + 10, 50, 30)),   # Green box
    (BLUE, pygame.Rect(130, HEIGHT + 10, 50, 30)),  # Blue box
]

# Initialize variables
dragging = False
dragging_ui_element = None
selected_color = None
deleted_cells = []

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check if the mouse is in the UI area
            if mouse_pos[1] >= HEIGHT:
                for i, (color, ui_element) in enumerate(ui_elements):
                    if ui_element.collidepoint(mouse_pos):
                        dragging_ui_element = i
                        break
            else:
                # Check if the mouse is on a grid cell
                grid_x = mouse_pos[0] // GRID_SIZE
                grid_y = mouse_pos[1] // GRID_SIZE
                if event.button == 1:  # Left mouse button
                    if grid[grid_y][grid_x] is not None:
                        # Start dragging an existing rectangle
                        dragging = True
                        selected_color = grid[grid_y][grid_x]
                        grid[grid_y][grid_x] = None
                    elif selected_color is not None:
                        # Place a new rectangle on the grid
                        grid[grid_y][grid_x] = selected_color
                elif event.button == 3:  # Right mouse button
                    if grid[grid_y][grid_x] is not None:
                        # Delete a rectangle from the grid
                        deleted_cells.append((grid_x, grid_y))
                        grid[grid_y][grid_x] = None

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                mouse_pos = pygame.mouse.get_pos()
                grid_x = mouse_pos[0] // GRID_SIZE
                grid_y = mouse_pos[1] // GRID_SIZE

                # Snap the dragged rectangle to the grid
                grid[grid_y][grid_x] = selected_color
                dragging = False
                selected_color = None

    screen.fill(WHITE)

    # Draw the grid
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    # Draw the rectangles on the grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] is not None:
                color = grid[y][x]
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, color, rect)

    # Draw the UI elements
    for i, (color, ui_element) in enumerate(ui_elements):
        pygame.draw.rect(screen, color, ui_element)
        if i == dragging_ui_element:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.rect(screen, color, (mouse_pos[0], mouse_pos[1], 50, 30))

    # Draw the deleted cells
    for x, y in deleted_cells:
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, GRAY, rect)

    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()

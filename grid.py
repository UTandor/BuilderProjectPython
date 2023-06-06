import pygame

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()

WIDTH = 800
HEIGHT = 600
GRID_SIZE = 50
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
UI_HEIGHT = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT + UI_HEIGHT))
pygame.display.set_caption("Grid Snap")

clock = pygame.time.Clock()

grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

ui_elements = [
    (RED, pygame.Rect(10, HEIGHT + 10, 50, 30)),   
    (GREEN, pygame.Rect(70, HEIGHT + 10, 50, 30)),   
    (BLUE, pygame.Rect(130, HEIGHT + 10, 50, 30)),  
]

dragging = False
dragging_ui_element = None
selected_color = None
deleted_cells = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if mouse_pos[1] >= HEIGHT:
                for i, (color, ui_element) in enumerate(ui_elements):
                    if ui_element.collidepoint(mouse_pos):
                        dragging_ui_element = i
                        break
            else:

                grid_x = mouse_pos[0] // GRID_SIZE
                grid_y = mouse_pos[1] // GRID_SIZE
                if event.button == 1:  
                    if grid[grid_y][grid_x] is not None:

                        dragging = True
                        selected_color = grid[grid_y][grid_x]
                        grid[grid_y][grid_x] = None
                    elif selected_color is not None:

                        grid[grid_y][grid_x] = selected_color
                elif event.button == 3:  
                    if grid[grid_y][grid_x] is not None:

                        deleted_cells.append((grid_x, grid_y))
                        grid[grid_y][grid_x] = None

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                mouse_pos = pygame.mouse.get_pos()
                grid_x = mouse_pos[0] // GRID_SIZE
                grid_y = mouse_pos[1] // GRID_SIZE

                grid[grid_y][grid_x] = selected_color
                dragging = False
                selected_color = None

    screen.fill(WHITE)

    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] is not None:
                color = grid[y][x]
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, color, rect)

    for i, (color, ui_element) in enumerate(ui_elements):
        pygame.draw.rect(screen, color, ui_element)
        if i == dragging_ui_element:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.rect(screen, color, (mouse_pos[0], mouse_pos[1], 50, 30))

    for x, y in deleted_cells:
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, GRAY, rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
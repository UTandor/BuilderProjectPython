import pygame
import math

GRID_SIZE = 50

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

rectangles = []

ui_buttons = [
    {"rect": pygame.Rect(screen_width // 2 - 185, screen_height - 60, 50, 50), "color": (255, 0, 0)},
    {"rect": pygame.Rect(screen_width // 2 - 125, screen_height - 60, 50, 50), "color": (0, 0, 255)},
    {"rect": pygame.Rect(screen_width // 2 - 65, screen_height - 60, 50, 50), "color": (255, 255, 0)},
    {"rect": pygame.Rect(screen_width // 2 - 5, screen_height - 60, 50, 50), "color": (255, 165, 0)},
    {"rect": pygame.Rect(screen_width // 2 + 55, screen_height - 60, 50, 50), "color": (0, 255, 0)},
    {"rect": pygame.Rect(screen_width // 2 + 115, screen_height - 60, 50, 50), "color": (128, 0, 128)}
]

ui_selected_button = None
preview_color = None

dragging_rect = None
dragging_offset = (0, 0)

def snap_to_grid(position):
    snapped_x = round((position[0] - GRID_SIZE / 2) / GRID_SIZE) * GRID_SIZE
    snapped_y = round((position[1] - GRID_SIZE / 2) / GRID_SIZE) * GRID_SIZE
    return (snapped_x, snapped_y)

def get_darker_color(color):
    r = max(color[0] - 50, 0)
    g = max(color[1] - 50, 0)
    b = max(color[2] - 50, 0)
    return (r, g, b)

font = pygame.font.SysFont(None, 24)
instructions = [
    "Left-click on a color button to select it.",
    "Left-click on the grid to place a rectangle.",
    "Right-click on a rectangle to delete it.",
    "Scroll the mouse wheel to switch colors.",
]
text_y = screen_height - 30
for instruction in instructions:
    text = font.render(instruction, True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, text_y))
    screen.blit(text, text_rect)
    text_y += 30

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, button in enumerate(ui_buttons):
                    if button["rect"].collidepoint(event.pos):
                        ui_selected_button = i
                        break
                else:
                    if ui_selected_button is not None:
                        mouse_pos = snap_to_grid(event.pos)
                        rect_width = GRID_SIZE
                        rect_height = GRID_SIZE
                        rect = pygame.Rect(mouse_pos[0], mouse_pos[1], rect_width, rect_height)
                        rect_color = ui_buttons[ui_selected_button]["color"]
                        rectangles.append((rect, rect_color))
            elif event.button == 3:
                for rect, _ in rectangles:
                    if rect.collidepoint(event.pos):
                        rectangles.remove((rect, _))
                        break
            elif event.button == 4:
                if ui_selected_button is not None:
                    ui_selected_button -= 1
                    if ui_selected_button < 0:
                        ui_selected_button = len(ui_buttons) - 1
            elif event.button == 5:
                if ui_selected_button is not None:
                    ui_selected_button += 1
                    if ui_selected_button >= len(ui_buttons):
                        ui_selected_button = 0

    screen.fill((255, 255, 255))

    for x in range(0, screen_width, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, screen_height))
    for y in range(0, screen_height, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (screen_width, y))

    for rect, color in rectangles:
        pygame.draw.rect(screen, color, rect)

    for i, button in enumerate(ui_buttons):
        pygame.draw.rect(screen, button["color"], button["rect"])
        if ui_selected_button == i:
            pygame.draw.rect(screen, (255, 255, 255), button["rect"], 3)

    if ui_selected_button is not None:
        mouse_pos = pygame.mouse.get_pos()
        snapped_pos = snap_to_grid(mouse_pos)
        rect_width = GRID_SIZE
        rect_height = GRID_SIZE
        preview_rect = pygame.Rect(snapped_pos[0], snapped_pos[1], rect_width, rect_height)
        if ui_selected_button != 4 and ui_selected_button != 5:
            preview_color = get_darker_color(ui_buttons[ui_selected_button]["color"])
        else:
            preview_color = ui_buttons[ui_selected_button]["color"]
        pygame.draw.rect(screen, preview_color, preview_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

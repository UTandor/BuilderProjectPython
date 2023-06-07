import pygame
import pygame_gui

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 50
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BARRACK_SIZE = 1

TROOP_SIZE = 0.5
TROOP_SPEED = 1

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Grid-based Game")

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Road Simulation")

road_image = pygame.image.load(ROAD_IMAGE_PATH)
road_image = pygame.transform.scale(road_image, (ROAD_SIZE, ROAD_SIZE))

class RoadObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rotation = 0

ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

UI_BUTTON_WIDTH = 100
UI_BUTTON_HEIGHT = 30
UI_BUTTON_PADDING = 10
UI_BUTTON_POSITION_X = (WINDOW_WIDTH - UI_BUTTON_WIDTH * 3 - UI_BUTTON_PADDING * 2) // 2
UI_BUTTON_POSITION_Y = WINDOW_HEIGHT - UI_BUTTON_HEIGHT - UI_BUTTON_PADDING

UI_BUTTON_COLORS = [RED, GREEN, BLUE]

road_objects = []

ui_visible = True
creating_road = False

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                if ui_visible:
                    if not creating_road:

                        creating_road = True
                        road_preview = RoadObject(*event.pos)
                    else:

                        road_preview.snap_to_grid()
                        road_objects.append(road_preview)
                        creating_road = False
                else:

                    road_objects.append(RoadObject(*event.pos))
            elif event.button == 3:  
                if not creating_road and not ui_visible:

                    for obj in road_objects:
                        if obj.x == event.pos[0] and obj.y == event.pos[1]:
                            road_objects.remove(obj)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:

                ui_visible = not ui_visible
            elif event.key == pygame.K_r:

                if creating_road and ui_visible:
                    road_preview.rotate()

    if creating_road:
        road_preview.x, road_preview.y = pygame.mouse.get_pos()

    screen.fill(BACKGROUND_COLOR)

    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    for obj in road_objects:
        obj.draw()

    if creating_road:
        road_preview.draw()

    if ui_visible:
        pygame.draw.rect(screen, UI_COLOR, (0, 0, UI_WIDTH, UI_HEIGHT))
        pygame.draw.rect(screen, UI_BORDER_COLOR, (0, 0, UI_WIDTH, UI_HEIGHT), 2)
        font = pygame.font.Font(None, 24)
        text = font.render(UI_TOGGLE_TEXT, True, (0, 0, 0))
        screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
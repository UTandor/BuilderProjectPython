import pygame
import math

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 50
ROAD_SIZE = GRID_SIZE
BACKGROUND_COLOR = (255, 255, 255)
GRID_COLOR = (200, 200, 200)
ROAD_COLOR = (0, 0, 0)
ROAD_IMAGE_PATH = "images/LineRoad.png"
UI_COLOR = (150, 150, 150)
UI_BORDER_COLOR = (100, 100, 100)
UI_WIDTH = 200
UI_HEIGHT = 50
UI_TOGGLE_TEXT = "Toggle UI (T)"

# Create the Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Road Simulation")

# Load road image and scale it down
road_image = pygame.image.load(ROAD_IMAGE_PATH)
road_image = pygame.transform.scale(road_image, (ROAD_SIZE, ROAD_SIZE))

# Define road object class
class RoadObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rotation = 0

    def draw(self):
        rotated_road = pygame.transform.rotate(road_image, self.rotation)
        screen.blit(rotated_road, (self.x, self.y))

    def snap_to_grid(self):
        self.x = round(self.x / GRID_SIZE) * GRID_SIZE
        self.y = round(self.y / GRID_SIZE) * GRID_SIZE

    def rotate(self):
        self.rotation = (self.rotation + 90) % 360

# Create road objects list
road_objects = []

# Initialize variables
ui_visible = True
creating_road = False

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if ui_visible:
                    if not creating_road:
                        # Start creating road object
                        creating_road = True
                        road_preview = RoadObject(*event.pos)
                    else:
                        # Place road object on the grid
                        road_preview.snap_to_grid()
                        road_objects.append(road_preview)
                        creating_road = False
                else:
                    # Place road object on the grid directly
                    road_objects.append(RoadObject(*event.pos))
            elif event.button == 3:  # Right mouse button
                if not creating_road and not ui_visible:
                    # Delete road object
                    for obj in road_objects:
                        if obj.x == event.pos[0] and obj.y == event.pos[1]:
                            road_objects.remove(obj)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                # Toggle UI visibility
                ui_visible = not ui_visible
            elif event.key == pygame.K_r:
                # Rotate road preview
                if creating_road and ui_visible:
                    road_preview.rotate()

    # Update road preview position
    if creating_road:
        road_preview.x, road_preview.y = pygame.mouse.get_pos()

    # Draw the background
    screen.fill(BACKGROUND_COLOR)

    # Draw the grid
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    # Draw the road objects
    for obj in road_objects:
        obj.draw()

    # Draw the road preview
    if creating_road:
        road_preview.draw()

    # Draw the UI element
    if ui_visible:
        pygame.draw.rect(screen, UI_COLOR, (0, 0, UI_WIDTH, UI_HEIGHT))
        pygame.draw.rect(screen, UI_BORDER_COLOR, (0, 0, UI_WIDTH, UI_HEIGHT), 2)
        font = pygame.font.Font(None, 24)
        text = font.render(UI_TOGGLE_TEXT, True, (0, 0, 0))
        screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()

# Quit the simulation
pygame.quit()

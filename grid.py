import pygame
import pygame_gui

# Initialize pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Grid dimensions
GRID_SIZE = 50
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Barrack properties
BARRACK_SIZE = 1

# Troop properties
TROOP_SIZE = 0.5
TROOP_SPEED = 1

# Initialize the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Grid-based Game")

# Game clock
clock = pygame.time.Clock()

# Game grid
grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Create the central orange box
central_box_x = GRID_WIDTH // 2 - 1
central_box_y = GRID_HEIGHT // 2 - 1
for i in range(2):
    for j in range(2):
        grid[central_box_y + i][central_box_x + j] = ORANGE

# Barracks list
barracks = []

# UI Manager
ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

# UI Button positions
UI_BUTTON_WIDTH = 100
UI_BUTTON_HEIGHT = 30
UI_BUTTON_PADDING = 10
UI_BUTTON_POSITION_X = (WINDOW_WIDTH - UI_BUTTON_WIDTH * 3 - UI_BUTTON_PADDING * 2) // 2
UI_BUTTON_POSITION_Y = WINDOW_HEIGHT - UI_BUTTON_HEIGHT - UI_BUTTON_PADDING

# UI Button colors
UI_BUTTON_COLORS = [RED, GREEN, BLUE]

# UI Toggle buttons
ui_toggle_buttons = []
for i, color in enumerate(UI_BUTTON_COLORS):
    button_rect = pygame.Rect(
        UI_BUTTON_POSITION_X + (UI_BUTTON_WIDTH + UI_BUTTON_PADDING) * i,
        UI_BUTTON_POSITION_Y,
        UI_BUTTON_WIDTH,
        UI_BUTTON_HEIGHT
    )
    button = pygame_gui.elements.UIButton(
        relative_rect=button_rect,
        text='',
        manager=ui_manager
    )
    button.bg_color = color
    button.selected = False
    ui_toggle_buttons.append(button)

# Selected barrack color
selected_color = None
selected_button = None

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for i, button in enumerate(ui_toggle_buttons):
                    if event.ui_element == button:
                        if selected_button == button:
                            selected_button = None
                            selected_color = None
                        else:
                            selected_button = button
                            selected_color = UI_BUTTON_COLORS[i]
                        break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and selected_color is not None:
                # Get the mouse position
                mouse_pos = pygame.mouse.get_pos()

                # Calculate the grid position
                grid_x = mouse_pos[0] // GRID_SIZE
                grid_y = mouse_pos[1] // GRID_SIZE

                # Check if the grid position is empty and within the valid range
                if (
                    0 <= grid_x < GRID_WIDTH
                    and 0 <= grid_y < GRID_HEIGHT
                    and grid[grid_y][grid_x] is None
                ):
                    # Create a new barrack
                    barrack = {
                        "x": grid_x,
                        "y": grid_y,
                        "color": selected_color,
                    }

                    # Add the barrack to the grid and barracks list
                    barracks.append(barrack)
                    grid[grid_y][grid_x] = barrack

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                if selected_button is not None:
                    index = ui_toggle_buttons.index(selected_button)
                    if index > 0:
                        selected_button = ui_toggle_buttons[index - 1]
                        selected_color = UI_BUTTON_COLORS[index - 1]
                    else:
                        selected_button = ui_toggle_buttons[-1]
                        selected_color = UI_BUTTON_COLORS[-1]
            elif event.button == 5:  # Scroll down
                if selected_button is not None:
                    index = ui_toggle_buttons.index(selected_button)
                    if index < len(ui_toggle_buttons) - 1:
                        selected_button = ui_toggle_buttons[index + 1]
                        selected_color = UI_BUTTON_COLORS[index + 1]
                    else:
                        selected_button = ui_toggle_buttons[0]
                        selected_color = UI_BUTTON_COLORS[0]

        ui_manager.process_events(event)

    # Update UI
    ui_manager.update(clock.tick(60) / 1000.0)

    # Clear the grid
    grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Update the grid with barracks
    for barrack in barracks:
        grid[barrack["y"]][barrack["x"]] = barrack

    # Draw the game
    window.fill(BLACK)

    # Draw the grid
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(window, ORANGE, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(window, ORANGE, (0, y), (WINDOW_WIDTH, y))

    # Draw the central box
    pygame.draw.rect(
        window,
        ORANGE,
        (
            central_box_x * GRID_SIZE,
            central_box_y * GRID_SIZE,
            2 * GRID_SIZE,
            2 * GRID_SIZE
        )
    )

    # Draw the barracks
    for barrack in barracks:
        pygame.draw.rect(
            window,
            barrack["color"],
            (barrack["x"] * GRID_SIZE, barrack["y"] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
        )

    # Draw the selected button outline
    if selected_button is not None:
        outline_rect = pygame.Rect(
            selected_button.rect.x - 2,
            selected_button.rect.y - 2,
            selected_button.rect.width + 4,
            selected_button.rect.height + 4,
        )
        pygame.draw.rect(window, (255, 255, 255), outline_rect, 2)

    # Draw the UI buttons
    ui_manager.draw_ui(window)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()

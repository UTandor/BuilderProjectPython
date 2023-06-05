import pygame

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Testing..........")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (0, 255, 0)  # Example color for hover
CLICK_COLOR = (0, 0, 255)  # Blue color for clicked state

class Rectangle():
    def __init__(self, scale, x_position, y_position, rect_color):
        self.scale = scale
        self.x_position = x_position
        self.y_position = y_position
        self.rect_color = rect_color
        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def render(self):
        pygame.draw.rect(screen, self.rect_color, (self.x_position, self.y_position, self.scale, self.scale))

    def check_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        rectangle_rect = pygame.Rect(self.x_position, self.y_position, self.scale, self.scale)
        if rectangle_rect.collidepoint(mouse_pos):
            if self.is_dragging:
                self.rect_color = CLICK_COLOR
            else:
                self.rect_color = HOVER_COLOR
        else:
            self.rect_color = RED

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            rectangle_rect = pygame.Rect(self.x_position, self.y_position, self.scale, self.scale)
            if rectangle_rect.collidepoint(mouse_pos):
                self.is_dragging = True
                self.offset_x = self.x_position - mouse_pos[0]
                self.offset_y = self.y_position - mouse_pos[1]
                self.rect_color = CLICK_COLOR
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                mouse_pos = pygame.mouse.get_pos()
                self.x_position = mouse_pos[0] + self.offset_x
                self.y_position = mouse_pos[1] + self.offset_y

                # Snap the rectangle to the grid
                k = 50  # Size of each grid square
                self.x_position = round(self.x_position / k) * k
                self.y_position = round(self.y_position / k) * k

# Create an instance of the Rectangle class
k = 50  # Size of each grid square
x_position = ((window_size[0] // k) // 2) * k  # Calculate x-coordinate for middle tile
y_position = ((window_size[1] // k) // 2) * k  # Calculate y-coordinate for middle tile
rectangle = Rectangle(k, x_position, y_position, BLACK)

running = True
while running:
    screen.fill(WHITE)

    # Draw the grid
    for x in range(0, window_size[0], k):
        pygame.draw.line(screen, (0, 0, 0, 100), (x, 0), (x, window_size[1]), 1)
    for y in range(0, window_size[1], k):
        pygame.draw.line(screen, (0, 0, 0, 100), (0, y), (window_size[0], y), 1)

    rectangle.render()
    rectangle.check_hover()

    font = pygame.font.Font(None, 36)
    text = font.render("You should be able to drag", True, BLACK)
    text_x = 10  # X-coordinate for top-left corner
    y_position = 10  # Y-coordinate for top-left corner

    screen.blit(text, (text_x, y_position))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        rectangle.handle_event(event)

    pygame.display.flip()

pygame.quit()

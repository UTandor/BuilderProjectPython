import pygame

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Grid Game")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (0, 255, 0)
CLICK_COLOR = (0, 0, 255)
UI_BACKGROUND_COLOR = (200, 200, 200)
UI_OUTLINE_COLOR = BLACK

class Rectangle:
    def __init__(self, scale, x_position, y_position, rect_color):
        self.scale = scale
        self.x_position = x_position
        self.y_position = y_position
        self.rect_color = rect_color
        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.marked_for_deletion = False

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
                if not self.is_dragging:
                    self.x_position = mouse_pos[0] - self.scale // 2
                    self.y_position = mouse_pos[1] - self.scale // 2
                self.is_dragging = True
                self.offset_x = self.x_position - mouse_pos[0]
                self.offset_y = self.y_position - mouse_pos[1]
                self.rect_color = CLICK_COLOR
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                if self.rect_color == CLICK_COLOR:
                    k = 50
                    self.x_position = round(self.x_position / k) * k
                    self.y_position = round(self.y_position / k) * k
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                mouse_pos = pygame.mouse.get_pos()
                self.x_position = mouse_pos[0] + self.offset_x
                self.y_position = mouse_pos[1] + self.offset_y
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_pos = pygame.mouse.get_pos()
            rectangle_rect = pygame.Rect(self.x_position, self.y_position, self.scale, self.scale)
            if rectangle_rect.collidepoint(mouse_pos):
                self.marked_for_deletion = True

class UIElement:
    def __init__(self, x_position, y_position, width, height, background_color, outline_color):
        self.x_position = x_position
        self.y_position = y_position
        self.width = width
        self.height = height
        self.background_color = background_color
        self.outline_color = outline_color

    def render(self):
        pygame.draw.rect(screen, self.outline_color, (self.x_position, self.y_position, self.width, self.height), 3)
        pygame.draw.rect(screen, self.background_color, (self.x_position + 3, self.y_position + 3, self.width - 6, self.height - 6))

    def check_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        element_rect = pygame.Rect(self.x_position, self.y_position, self.width, self.height)
        if element_rect.collidepoint(mouse_pos):
            self.outline_color = HOVER_COLOR
        else:
            self.outline_color = BLACK

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            element_rect = pygame.Rect(self.x_position, self.y_position, self.width, self.height)
            if element_rect.collidepoint(mouse_pos):
                rectangle = Rectangle(50, mouse_pos[0], mouse_pos[1], RED)
                rectangles.append(rectangle)

k = 50
x_position = ((window_size[0] // k) // 2) * k
y_position = ((window_size[1] // k) // 2) * k
rectangle = Rectangle(k, x_position, y_position, BLACK)

ui_element = UIElement(window_size[0] - 120, window_size[1] - 120, 100, 100, UI_BACKGROUND_COLOR, UI_OUTLINE_COLOR)

rectangles = []

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        rectangle.handle_event(event)
        ui_element.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for rect in rectangles:
                rect.handle_event(event)

    # Remove the marked rectangles
    rectangles = [rect for rect in rectangles if not rect.marked_for_deletion]

    screen.fill(WHITE)

    for x in range(0, window_size[0], k):
        pygame.draw.line(screen, (0, 0, 0, 100), (x, 0), (x, window_size[1]), 1)
    for y in range(0, window_size[1], k):
        pygame.draw.line(screen, (0, 0, 0, 100), (0, y), (window_size[0], y), 1)

    for rect in rectangles:
        rect.render()
        rect.check_hover()
        rect.handle_event(event)

    rectangle.render()
    rectangle.check_hover()

    ui_element.render()
    ui_element.check_hover()

    font = pygame.font.Font(None, 36)
    text = font.render("You can drag rectangles", True, BLACK)
    text_x = 10
    text_y = 10
    screen.blit(text, (text_x, text_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

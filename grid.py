import pygame

pygame.init()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Testing..........")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (0, 255, 0)  
CLICK_COLOR = (0, 0, 255)  

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

                if self.x_position < 0:
                    self.x_position = 0
                if self.x_position + self.scale > window_size[0]:
                    self.x_position = window_size[0] - self.scale
                if self.y_position < 0:
                    self.y_position = 0
                if self.y_position + self.scale > window_size[1]:
                    self.y_position = window_size[1] - self.scale

rectangle_width = 100
rectangle_height = 100
x_position = (window_size[0] - rectangle_width) // 2  
y_position = (window_size[1] - rectangle_height) // 2  
rectangle = Rectangle(rectangle_width, x_position, y_position, BLACK)

running = True
while running:
    screen.fill(WHITE)
    rectangle.render()
    rectangle.check_hover()

    font = pygame.font.Font(None, 36)
    text = font.render("You should be able to drag", True, BLACK)
    text_x = 10  
    y_position = 10  

    screen.blit(text, (text_x, y_position))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        rectangle.handle_event(event)

    pygame.display.flip()

pygame.quit()
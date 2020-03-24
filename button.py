import pygame


class Button:

    def __init__(self, x, y, w, h, text='', border=0,
                 color=pygame.Color('white'), textColor=pygame.Color('black'), editable=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.border = border
        self.color = color
        self.textColor = textColor
        self.text = text
        self.font = pygame.font.SysFont("comicsansms", 30)
        self.txt_surface = self.font.render(text, True, self.textColor)
        self.active = False
        self.textOffset_y = (h + border*2) // 2 - self.font.size(text)[1] // 2
        self.textOffset_x = (w + border*2) // 2 - self.font.size(text)[0] // 2
        self.color_inactive = self.color
        self.color_active = pygame.Color('dodgerblue2')

    def negate_active(self):
        self.active = False
        self.color = self.color_active if self.active else self.color_inactive

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        self.color = self.color_active if self.active else self.color_inactive

    def update(self):
        # Resize the box if the text is too long.
        width = max(300, self.txt_surface.get_width()+40)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, self.border)
        screen.blit(self.txt_surface, (self.rect.x + self.textOffset_x, self.rect.y + self.textOffset_y))

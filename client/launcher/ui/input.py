import pygame

class TextInput:
    def __init__(
        self,
        x,
        y,
        w,
        h,
        password=False,
        font_size=18,
        text_color=(255, 255, 255),
        max_length=20
    ):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.active = False
        self.password = password
        self.font = pygame.font.SysFont("arial", font_size)
        self.text_color = text_color
        self.max_length = max_length

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_length:
                # evita caracteres estranhos invisíveis
                if event.unicode.isprintable():
                    self.text += event.unicode

    def draw(self, screen):
        display_text = "*" * len(self.text) if self.password else self.text
        txt_surface = self.font.render(display_text, True, self.text_color)

        # centraliza verticalmente no input
        text_y = self.rect.y + (self.rect.height - txt_surface.get_height()) // 2
        screen.blit(txt_surface, (self.rect.x + 5, text_y))

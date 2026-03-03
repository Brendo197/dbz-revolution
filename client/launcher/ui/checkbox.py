import pygame

class Checkbox:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.checked = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked

    def draw(self, screen):
        # borda
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 1)

        # marcado
        if self.checked:
            pygame.draw.line(
                screen, (255, 255, 255),
                self.rect.topleft, self.rect.bottomright, 2
            )
            pygame.draw.line(
                screen, (255, 255, 255),
                self.rect.topright, self.rect.bottomleft, 2
            )

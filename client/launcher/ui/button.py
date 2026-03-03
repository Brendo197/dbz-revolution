import pygame

class InvisibleButton:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN and
            self.rect.collidepoint(event.pos)
        )

    def draw(self, screen):
        # DEBUG (descomente se quiser ver área)
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
        pass

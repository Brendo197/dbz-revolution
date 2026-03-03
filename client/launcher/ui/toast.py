import pygame
import time


class Toast:
    def __init__(self, screen_width):
        self.text = ""
        self.color = (255, 255, 255)
        self.start_time = 0
        self.duration = 0
        self.font = pygame.font.SysFont("arial", 16)
        self.active = False
        self.screen_width = screen_width

    def show(self, text, color=(255, 255, 255), duration=2.5):
        self.text = text
        self.color = color
        self.start_time = time.time()
        self.duration = duration
        self.active = True

    def draw(self, screen):
        if not self.active:
            return

        elapsed = time.time() - self.start_time
        if elapsed > self.duration:
            self.active = False
            return

        # Fade in / out
        alpha = 180
        if elapsed < 0.3:
            alpha = int(180 * (elapsed / 0.3))
        elif elapsed > self.duration - 0.3:
            alpha = int(180 * ((self.duration - elapsed) / 0.3))

        # Render text
        text_surface = self.font.render(self.text, True, self.color)
        padding_x = 20
        padding_y = 10

        box_width = text_surface.get_width() + padding_x * 2
        box_height = text_surface.get_height() + padding_y * 2

        x = (self.screen_width - box_width) // 2
        y = 20  # topo da tela

        # Background (semi-transparente)
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, alpha))

        # Desenhar bordas arredondadas (fake cloud)
        pygame.draw.rect(
            box_surface,
            (0, 0, 0, alpha),
            box_surface.get_rect(),
            border_radius=12
        )

        screen.blit(box_surface, (x, y))
        screen.blit(
            text_surface,
            (x + padding_x, y + padding_y)
        )

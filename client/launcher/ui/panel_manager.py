import pygame


class PanelManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.active_panel = None
        self.alpha = 0
        self.anim_speed = 600  # velocidade fade

        self.font = pygame.font.SysFont("arial", 28, bold=True)

        self.panel_rect = pygame.Rect(
            screen_width // 2 - 300,
            screen_height // 2 - 200,
            600,
            400
        )

    def open(self, panel_name):
        self.active_panel = panel_name
        self.alpha = 0

    def close(self):
        self.active_panel = None

    def update(self, dt):
        if self.active_panel and self.alpha < 200:
            self.alpha += self.anim_speed * dt
            if self.alpha > 200:
                self.alpha = 200

    def draw(self, screen):
        if not self.active_panel:
            return

        overlay = pygame.Surface(
            (self.screen_width, self.screen_height),
            pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        panel_surface = pygame.Surface(
            (self.panel_rect.width, self.panel_rect.height),
            pygame.SRCALPHA
        )
        panel_surface.fill((30, 35, 55, int(self.alpha)))

        screen.blit(panel_surface, self.panel_rect.topleft)

        title = self.font.render(
            self.active_panel.upper(),
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(self.panel_rect.centerx,
                    self.panel_rect.y + 40)
        )

        screen.blit(title, title_rect)
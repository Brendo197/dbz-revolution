import pygame


class MissionPanel:
    BASE_WIDTH = 1280
    BASE_HEIGHT = 704

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # ===== ESCALA =====
        self.scale_x = screen_width / self.BASE_WIDTH
        self.scale_y = screen_height / self.BASE_HEIGHT

        def sx(value): return int(value * self.scale_x)
        def sy(value): return int(value * self.scale_y)

        self.sx = sx
        self.sy = sy

        # ===== DIMENSÕES BASE =====
        base_width = 280
        base_height = 200
        base_x = 20
        base_y = 100

        self.width = sx(base_width)
        self.height = sy(base_height)
        self.x = sx(base_x)
        self.y = sy(base_y)

        self.bg_color = (25, 30, 45)
        self.border_color = (70, 90, 140)

        self.font_title = pygame.font.SysFont("arial", sy(18), bold=True)
        self.font_text = pygame.font.SysFont("arial", sy(14))

        # Missões fake
        self.missions = [
            "Derrote 10 inimigos",
            "Complete 3 batalhas",
            "Evolua 1 guerreiro"
        ]

    def draw(self, screen):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)

        pygame.draw.rect(screen, self.bg_color, rect, border_radius=10)
        pygame.draw.rect(screen, self.border_color, rect, 2, border_radius=10)

        title = self.font_title.render("MISSOES", True, (255, 255, 255))
        screen.blit(title, (self.x + self.sx(15), self.y + self.sy(10)))

        for i, mission in enumerate(self.missions):
            text = self.font_text.render(mission, True, (200, 200, 200))
            screen.blit(
                text,
                (
                    self.x + self.sx(15),
                    self.y + self.sy(45) + i * self.sy(25)
                )
            )
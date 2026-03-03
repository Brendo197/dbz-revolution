import pygame
from core.config_manager import load_config


RESOLUTIONS = {
    1: (800, 608),
    2: (1280, 704),
    3: (1344, 704),
    4: (1600, 832),
    5: (1856, 960),
    6: (2432, 960),
}


class ConfigPanel:
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

        # ===== TAMANHO BASE =====
        base_width = 600
        base_height = 400

        self.width = sx(base_width)
        self.height = sy(base_height)

        self.rect = pygame.Rect(
            screen_width // 2 - self.width // 2,
            screen_height // 2 - self.height // 2,
            self.width,
            self.height
        )

        # ===== FONTES ESCALADAS =====
        self.font = pygame.font.SysFont("arial", sy(22))
        self.small_font = pygame.font.SysFont("arial", sy(18))

        config = load_config()
        self.selected_resolution = config.get("resolution", 2)

        self.dropdown_open = False

        # guarda funções escala
        self.sx = sx
        self.sy = sy

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = event.pos

            dropdown_rect = pygame.Rect(
                self.rect.x + self.sx(200),
                self.rect.y + self.sy(120),
                self.sx(200),
                self.sy(35)
            )

            if dropdown_rect.collidepoint(mouse):
                self.dropdown_open = not self.dropdown_open
                return None

            if self.dropdown_open:
                for i, (key, value) in enumerate(RESOLUTIONS.items()):
                    option_rect = pygame.Rect(
                        self.rect.x + self.sx(200),
                        self.rect.y + self.sy(160 + i * 35),
                        self.sx(200),
                        self.sy(30)
                    )

                    if option_rect.collidepoint(mouse):
                        self.selected_resolution = key
                        self.dropdown_open = False
                        return key, value

        return None

    def draw(self, screen):
        pygame.draw.rect(screen, (30, 35, 55), self.rect, border_radius=10)

        title = self.font.render("CONFIGURAÇÕES", True, (255, 255, 255))
        screen.blit(title, (self.rect.x + self.sx(20), self.rect.y + self.sy(20)))

        label = self.small_font.render("Resolução:", True, (200, 200, 200))
        screen.blit(label, (self.rect.x + self.sx(50), self.rect.y + self.sy(125)))

        dropdown_rect = pygame.Rect(
            self.rect.x + self.sx(200),
            self.rect.y + self.sy(120),
            self.sx(200),
            self.sy(35)
        )

        pygame.draw.rect(screen, (50, 60, 90), dropdown_rect, border_radius=5)

        res_text = self.small_font.render(
            f"{RESOLUTIONS[self.selected_resolution][0]}x{RESOLUTIONS[self.selected_resolution][1]}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            res_text,
            (dropdown_rect.x + self.sx(10),
             dropdown_rect.y + self.sy(7))
        )

        if self.dropdown_open:
            for i, (key, value) in enumerate(RESOLUTIONS.items()):
                option_rect = pygame.Rect(
                    self.rect.x + self.sx(200),
                    self.rect.y + self.sy(160 + i * 35),
                    self.sx(200),
                    self.sy(30)
                )

                pygame.draw.rect(screen, (40, 45, 70), option_rect)

                text = self.small_font.render(
                    f"{value[0]}x{value[1]}",
                    True,
                    (255, 255, 255)
                )

                screen.blit(
                    text,
                    (option_rect.x + self.sx(10),
                     option_rect.y + self.sy(5))
                )
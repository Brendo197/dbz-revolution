import pygame
from game.session import session


class TopBar:
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

        # ===== DIMENSÕES =====
        self.width = screen_width
        self.height = sy(75)

        self.bg_color = (18, 22, 32)
        self.accent = (255, 170, 0)

        # Fontes escaladas
        self.font_big = pygame.font.SysFont("arial", sy(22), bold=True)
        self.font_small = pygame.font.SysFont("arial", sy(16))

    def draw(self, screen):
        # Fundo
        pygame.draw.rect(screen, self.bg_color,
                         (0, 0, self.width, self.height))

        nickname = getattr(session, "nickname", "Player")
        level = getattr(session, "level", 1)
        zeny = getattr(session, "bank_zeny", 0)
        vip_days = getattr(session, "vip_days", 0)

        # Nome
        name_text = self.font_big.render(nickname, True, (255, 255, 255))
        screen.blit(name_text, (self.sx(20), self.sy(12)))

        # Level
        level_text = self.font_small.render(
            f"Lv {level}", True, self.accent)
        screen.blit(level_text, (self.sx(20), self.sy(42)))

        # Zeny
        zeny_text = self.font_small.render(
            f"Zeny: {zeny}", True, (255, 255, 255))
        screen.blit(zeny_text, (self.sx(250), self.sy(30)))

        # VIP
        if vip_days > 0:
            vip_text = self.font_small.render(
                "VIP", True, (255, 215, 0))
            screen.blit(vip_text, (self.sx(450), self.sy(30)))
import pygame


class BottomMenu:
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

        # ===== DIMENSÕES =====
        self.height = sy(90)
        self.y = screen_height - self.height

        self.bg_color = (18, 22, 32)
        self.button_color = (40, 45, 65)
        self.hover_color = (70, 80, 120)
        self.text_color = (255, 255, 255)

        # Fonte proporcional
        self.font = pygame.font.SysFont("arial", sy(18), bold=True)
        self.icon_font = pygame.font.SysFont("arial", sy(24))

        # ===== BOTÕES PRINCIPAIS =====
        self.buttons = []
        names = ["INVENTARIO", "HISTORIA", "GUERREIROS", "ARENA"]

        spacing = sx(20)
        btn_width = sx(160)
        btn_height = sy(45)

        total_width = len(names) * btn_width + (len(names) - 1) * spacing
        start_x = (screen_width - total_width) // 2

        for i, name in enumerate(names):
            rect = pygame.Rect(
                start_x + i * (btn_width + spacing),
                self.y + sy(22),
                btn_width,
                btn_height
            )
            self.buttons.append((name.lower(), rect))

        # ===== BOTÃO CONFIG (topo direito) =====
        self.config_button = pygame.Rect(
            screen_width - sx(60),
            sy(15),
            sx(40),
            sy(40)
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.config_button.collidepoint(event.pos):
                return "config"

            for name, rect in self.buttons:
                if rect.collidepoint(event.pos):
                    return name

        return None

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # ===== BARRA INFERIOR =====
        pygame.draw.rect(
            screen,
            self.bg_color,
            (0, self.y, self.screen_width, self.height)
        )

        # ===== BOTÕES PRINCIPAIS =====
        for name, rect in self.buttons:
            color = (
                self.hover_color
                if rect.collidepoint(mouse_pos)
                else self.button_color
            )

            pygame.draw.rect(screen, color, rect, border_radius=8)

            text = self.font.render(name.upper(), True, self.text_color)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # ===== BOTÃO CONFIG =====
        color = (
            self.hover_color
            if self.config_button.collidepoint(mouse_pos)
            else self.button_color
        )

        pygame.draw.rect(
            screen,
            color,
            self.config_button,
            border_radius=8
        )

        icon = self.icon_font.render("⚙", True, self.text_color)
        icon_rect = icon.get_rect(center=self.config_button.center)
        screen.blit(icon, icon_rect)
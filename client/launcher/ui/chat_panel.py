import pygame
from game.session import session


class ChatPanel:
    BASE_WIDTH = 1280
    BASE_HEIGHT = 704

    MAX_MESSAGE_LENGTH = 120
    CHANNELS = ["global", "system", "guild"]

    def __init__(self, screen_width, screen_height, bottom_menu_height):

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.scale_x = screen_width / self.BASE_WIDTH
        self.scale_y = screen_height / self.BASE_HEIGHT

        def sx(v): return int(v * self.scale_x)
        def sy(v): return int(v * self.scale_y)

        self.sx = sx
        self.sy = sy

        base_width = 420
        base_height = 220

        self.width = sx(base_width)
        self.height = sy(base_height)

        self.x = sx(20)
        self.y = screen_height - bottom_menu_height - self.height - sy(10)

        self.font = pygame.font.SysFont("arial", sy(14))
        self.tab_font = pygame.font.SysFont("arial", sy(13), bold=True)

        self.line_height = sy(20)
        usable_height = self.height - sy(70)
        self.max_visible_lines = max(1, usable_height // self.line_height)

        self.active_channel = "global"
        session.active_chat_channel = "global"

        self.scroll_offset = {c: 0 for c in self.CHANNELS}

        self.input_text = ""
        self.active = False

        # badge blink
        self.badge_timer = 0
        self.badge_visible = True

        # cursor
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 0.5

    # =====================================================
    # EVENTOS
    # =====================================================

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = event.pos

            for i, channel in enumerate(self.CHANNELS):
                if self.get_tab_rect(i).collidepoint(mouse):
                    self.active_channel = channel
                    session.active_chat_channel = channel

                    # limpa unread ao abrir
                    session.chat_unread[channel] = 0
                    return None

            # 🚫 BLOQUEIA INPUT NA ABA SYSTEM
            if self.active_channel != "system":
                self.active = self.get_input_rect().collidepoint(mouse)
            else:
                self.active = False

        if event.type == pygame.MOUSEWHEEL:
            total_lines = self.get_total_lines()
            max_scroll = max(0, total_lines - self.max_visible_lines)

            self.scroll_offset[self.active_channel] -= event.y
            self.scroll_offset[self.active_channel] = max(
                0,
                min(self.scroll_offset[self.active_channel], max_scroll)
            )

        if event.type == pygame.KEYDOWN and self.active:

            if event.key == pygame.K_RETURN:
                if self.input_text.strip():
                    msg = self.input_text.strip()
                    self.input_text = ""
                    return msg

            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]

            else:
                if len(self.input_text) < self.MAX_MESSAGE_LENGTH:
                    self.input_text += event.unicode

        return None

    # =====================================================
    # UTILS
    # =====================================================

    def get_tab_rect(self, index):
        tab_width = self.width // len(self.CHANNELS)
        return pygame.Rect(
            self.x + index * tab_width,
            self.y,
            tab_width,
            self.sy(30)
        )

    def get_input_rect(self):
        return pygame.Rect(
            self.x,
            self.y + self.height - self.sy(35),
            self.width,
            self.sy(30)
        )

    def get_total_lines(self):
        messages = session.chat_messages[self.active_channel]
        max_width = self.width - self.sx(25)
        total = 0

        for nickname, message in messages:
            total += len(self.wrap_text(nickname + ": " + message, max_width))

        return total

    def wrap_text(self, text, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word

            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, screen, dt):

        # badge blink
        self.badge_timer += dt
        if self.badge_timer >= 0.5:
            self.badge_timer = 0
            self.badge_visible = not self.badge_visible

        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        pygame.draw.rect(screen, (20, 24, 35), panel_rect, border_radius=10)
        pygame.draw.rect(screen, (60, 80, 120), panel_rect, 2, border_radius=10)

        # ===== ABAS =====
        for i, channel in enumerate(self.CHANNELS):
            rect = self.get_tab_rect(i)

            color = (80, 110, 200) if channel == self.active_channel else (40, 45, 60)
            pygame.draw.rect(screen, color, rect)

            text = self.tab_font.render(channel.upper(), True, (255, 255, 255))
            screen.blit(
                text,
                (
                    rect.centerx - text.get_width() // 2,
                    rect.centery - text.get_height() // 2
                )
            )

            # 🔴 BADGE
            unread = session.chat_unread[channel]
            if unread > 0 and channel != self.active_channel and self.badge_visible:

                badge_radius = self.sy(8)
                badge_x = rect.right - self.sy(15)
                badge_y = rect.y + self.sy(8)

                pygame.draw.circle(screen, (220, 40, 40), (badge_x, badge_y), badge_radius)

        # ===== MENSAGENS =====
        messages = session.chat_messages[self.active_channel]
        max_width = self.width - self.sx(25)

        wrapped_lines = []
        for nickname, message in messages:
            lines = self.wrap_text(nickname + ": " + message, max_width)
            for i, line in enumerate(lines):
                if i == 0:
                    wrapped_lines.append((nickname, line))
                else:
                    wrapped_lines.append((None, line))

        total_lines = len(wrapped_lines)
        max_scroll = max(0, total_lines - self.max_visible_lines)

        offset = self.scroll_offset[self.active_channel]
        offset = max(0, min(offset, max_scroll))

        start = max(0, total_lines - self.max_visible_lines - offset)
        end = total_lines - offset

        visible_lines = wrapped_lines[start:end]

        for i, (nickname, line) in enumerate(visible_lines):

            y = self.y + self.sy(40) + i * self.line_height
            x = self.x + self.sx(10)

            # ==============================
            # SISTEMA
            # ==============================
            if nickname == "Sistema":

                name_surface = self.font.render("Sistema:", True, (255, 120, 120))
                screen.blit(name_surface, (x, y))

                msg_surface = self.font.render(
                    line[len(nickname) + 2:], True, (220, 220, 220)
                )
                screen.blit(msg_surface, (x + name_surface.get_width(), y))

            # ==============================
            # PLAYER NORMAL
            # ==============================
            elif nickname:

                # 🔵 Nome azul
                name_surface = self.font.render(nickname + ":", True, (100, 160, 255))
                screen.blit(name_surface, (x, y))

                # ⚪ Texto branco
                msg_surface = self.font.render(
                    line[len(nickname) + 2:], True, (255, 255, 255)
                )
                screen.blit(msg_surface, (x + name_surface.get_width(), y))

            # ==============================
            # CONTINUAÇÃO DE LINHA
            # ==============================
            else:
                msg_surface = self.font.render(line, True, (255, 255, 255))
                screen.blit(msg_surface, (x, y))

        # ===== INPUT =====
        input_rect = self.get_input_rect()

        # visual bloqueado na aba system
        if self.active_channel == "system":
            pygame.draw.rect(screen, (30, 30, 30), input_rect)
        else:
            pygame.draw.rect(screen, (40, 45, 70), input_rect)

        if self.active_channel != "system":

            display_text = self.input_text

            if self.active:
                display_text += "|"

            clipped = display_text
            while self.font.size(clipped)[0] > input_rect.width - self.sx(15):
                clipped = clipped[1:]

            text_surface = self.font.render(clipped, True, (255, 255, 255))
            screen.blit(
                text_surface,
                (input_rect.x + self.sx(8),
                 input_rect.y + self.sy(5))
            )
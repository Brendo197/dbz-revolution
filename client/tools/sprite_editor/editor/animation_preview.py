import pygame
from tools.sprite_editor.core.animation_player import AnimationPlayer

MAX_OFFSET = 2000


class AnimationPreview:

    def __init__(self, editor):

        self.editor = editor
        self.player = AnimationPlayer()

        # modo edição
        self.fullscreen = False
        self.playing = True

        # drag
        self.dragging = False
        self.dragging_pivot = False
        self.drag_start = (0, 0)
        self.drag_offset_start = (0, 0)

        # botões
        self.buttons = []

        self.font = pygame.font.SysFont("consolas", 12)

    # ------------------------------------------------
    # UPDATE
    # ------------------------------------------------

    def update(self, dt):

        anim = self.editor.state.get_current_animation()
        if not anim or not anim.frames:
            return

        if self.player.animation != anim:
            self.player.play(anim)

        # modo normal → timeline manda
        if not self.fullscreen:

            idx = self.editor.state.current_frame_index

            if idx is not None:
                self.player.set_frame(idx)

            self.player.update(dt)

        # modo F → preview manda
        else:

            if self.playing:
                self.player.update(dt)

            self.editor.state.set_frame(self.player.frame_index)

    # ------------------------------------------------
    # INPUT
    # ------------------------------------------------

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_f:
                self.fullscreen = not self.fullscreen

            elif event.key == pygame.K_SPACE:
                self.playing = not self.playing

            elif event.key == pygame.K_RIGHT:
                self.next_frame()

            elif event.key == pygame.K_LEFT:
                self.prev_frame()

            elif event.key == pygame.K_r:
                self.reset()

            if self.fullscreen:

                if event.key == pygame.K_w:
                    self.adjust_offset(0, -1)

                elif event.key == pygame.K_s:
                    self.adjust_offset(0, 1)

                elif event.key == pygame.K_a:
                    self.adjust_offset(-1, 0)

                elif event.key == pygame.K_d:
                    self.adjust_offset(1, 0)

        # -------------------------
        # MOUSE
        # -------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = pygame.mouse.get_pos()
            rect = self.get_preview_rect()

            if not rect.collidepoint(mx, my):
                return

            # botões
            for r, action in self.buttons:

                if r.collidepoint(mx, my):

                    if action == "prev":
                        self.prev_frame()

                    elif action == "next":
                        self.next_frame()

                    elif action == "play":
                        self.playing = not self.playing

                    return

            if event.button == 1 and self.fullscreen:

                frame = self.player.get_frame()
                if not frame:
                    return

                self.playing = False
                self.drag_start = (mx, my)

                keys = pygame.key.get_pressed()

                # 🔵 pivot
                if keys[pygame.K_LSHIFT]:

                    self.dragging_pivot = True
                    self.drag_offset_start = (
                        frame.origin_x,
                        frame.origin_y
                    )

                # 🟢 offset
                else:

                    self.dragging = True
                    self.drag_offset_start = (
                        frame.offset_x,
                        frame.offset_y
                    )

                self.editor.state.set_frame(self.player.frame_index)

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            self.dragging_pivot = False

        if event.type == pygame.MOUSEMOTION:

            if not (self.dragging or self.dragging_pivot):
                return

            mx, my = pygame.mouse.get_pos()

            dx = mx - self.drag_start[0]
            dy = my - self.drag_start[1]

            frame = self.player.get_frame()
            if not frame:
                return

            # OFFSET
            if self.dragging:

                new_x = self.drag_offset_start[0] + dx
                new_y = self.drag_offset_start[1] + dy

                frame.offset_x = max(-MAX_OFFSET, min(MAX_OFFSET, new_x))
                frame.offset_y = max(-MAX_OFFSET, min(MAX_OFFSET, new_y))

            # PIVOT
            if self.dragging_pivot:
                new_x = self.drag_offset_start[0] - dx
                new_y = self.drag_offset_start[1] - dy

                frame.origin_x = max(-MAX_PIVOT, min(MAX_PIVOT, new_x))
                frame.origin_y = max(-MAX_PIVOT, min(MAX_PIVOT, new_y))

            self.editor.state.set_frame(self.player.frame_index)

    # ------------------------------------------------
    # RESET
    # ------------------------------------------------

    def reset(self):

        self.editor.state.set_frame(0)
        self.player.set_frame(0)

    # ------------------------------------------------
    # OFFSET
    # ------------------------------------------------

    def adjust_offset(self, dx, dy):

        frame = self.player.get_frame()
        if not frame:
            return

        keys = pygame.key.get_pressed()
        speed = 5 if keys[pygame.K_LSHIFT] else 1

        frame.offset_x = max(
            -MAX_OFFSET,
            min(MAX_OFFSET, frame.offset_x + dx * speed)
        )

        frame.offset_y = max(
            -MAX_OFFSET,
            min(MAX_OFFSET, frame.offset_y + dy * speed)
        )

        self.editor.state.set_frame(self.player.frame_index)

    # ------------------------------------------------
    # FRAME CONTROL
    # ------------------------------------------------

    def next_frame(self):

        anim = self.player.animation
        if not anim:
            return

        idx = self.editor.state.current_frame_index or 0
        idx = (idx + 1) % len(anim.frames)

        self.editor.state.set_frame(idx)
        self.player.set_frame(idx)

    def prev_frame(self):

        anim = self.player.animation
        if not anim:
            return

        idx = self.editor.state.current_frame_index or 0
        idx = (idx - 1) % len(anim.frames)

        self.editor.state.set_frame(idx)
        self.player.set_frame(idx)

    # ------------------------------------------------
    # PREVIEW AREA
    # ------------------------------------------------

    def get_preview_rect(self):

        return self.editor.layout.canvas if self.fullscreen else self.editor.layout.preview

    # ------------------------------------------------
    # DRAW FRAME
    # ------------------------------------------------

    def draw_frame(self, screen, frame, rect, sheet, alpha=255):

        try:
            img = sheet.subsurface(
                int(frame.x),
                int(frame.y),
                int(frame.w),
                int(frame.h)
            )
        except:
            return None

        img = img.copy()

        if alpha != 255:
            img.set_alpha(alpha)

        ground_y = rect.bottom - 64
        pivot_x = rect.centerx
        pivot_y = ground_y

        draw_x = pivot_x - frame.origin_x + frame.offset_x
        draw_y = pivot_y - frame.origin_y + frame.offset_y

        screen.blit(img, (draw_x, draw_y))

        return draw_x, draw_y, frame.w, frame.h

    # ------------------------------------------------
    # PLAYER UI
    # ------------------------------------------------

    def draw_player(self, screen, rect):

        self.buttons.clear()

        y = rect.bottom - 36
        x = rect.centerx - 80

        buttons = [
            ("◀", "prev"),
            ("PLAY" if not self.playing else "PAUSE", "play"),
            ("▶", "next")
        ]

        for label, action in buttons:

            r = pygame.Rect(x, y, 70, 26)

            pygame.draw.rect(screen, (60, 60, 60), r)
            pygame.draw.rect(screen, (120, 120, 120), r, 1)

            txt = self.font.render(label, True, (220, 220, 220))
            screen.blit(txt, (r.centerx - txt.get_width() / 2, r.y + 5))

            self.buttons.append((r, action))

            x += 80

    # ------------------------------------------------
    # DRAW
    # ------------------------------------------------

    def draw(self, screen):

        frame = self.player.get_frame()
        if not frame:
            return

        sheet = self.editor.canvas.sheet
        if not sheet:
            return

        rect = self.get_preview_rect()

        pygame.draw.rect(screen, (26, 26, 26), rect)

        # grid
        if self.fullscreen:

            for x in range(rect.left, rect.right, 32):
                pygame.draw.line(screen, (45, 45, 45), (x, rect.top), (x, rect.bottom))

            for y in range(rect.top, rect.bottom, 32):
                pygame.draw.line(screen, (45, 45, 45), (rect.left, y), (rect.right, y))

        # onion
        if self.fullscreen:

            anim = self.player.animation

            if anim and len(anim.frames) > 1:
                prev = anim.frames[(self.player.frame_index - 1) % len(anim.frames)]
                self.draw_frame(screen, prev, rect, sheet, alpha=70)

        result = self.draw_frame(screen, frame, rect, sheet)
        if not result:
            return

        draw_x, draw_y, w, h = result

        # chão
        ground_y = rect.bottom - 64
        pygame.draw.line(screen, (80, 80, 80), (rect.left, ground_y), (rect.right, ground_y), 2)

        # pivot visual
        if self.fullscreen:
            cx = rect.centerx
            cy = ground_y

            pygame.draw.line(screen, (0, 200, 255), (cx - 10, cy), (cx + 10, cy), 2)
            pygame.draw.line(screen, (0, 200, 255), (cx, cy - 10), (cx, cy + 10), 2)

        # hit
        if frame.attack_frame:
            pygame.draw.rect(screen, (255, 80, 80), (draw_x, draw_y, w, h), 2)

        # HUD
        anim = self.player.animation

        info = f"{self.player.frame_index}/{len(anim.frames)}"
        txt = self.font.render(info, True, (200, 200, 200))
        screen.blit(txt, (rect.left + 6, rect.top + 4))

        if self.fullscreen:
            self.draw_player(screen, rect)
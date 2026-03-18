import pygame


class Timeline:

    def __init__(self, editor):

        self.editor = editor
        self.state = editor.state

        self.frame_size = 64
        self.frame_margin = 12

        self.frame_rects = []

        # scroll
        self.scroll_x = 0
        self.scroll_speed = 40

        # drag timeline
        self.drag_scroll = False

        # drag reorder
        self.dragging = False
        self.drag_index = None

        # hover
        self.hover_index = None

        # font cache
        self.font = pygame.font.SysFont("arial", 12)

    # -------------------------
    # EVENTS
    # -------------------------

    def handle_event(self, event):

        layout = self.editor.layout
        timeline_rect = layout.timeline

        mx, my = pygame.mouse.get_pos()

        # -------------------------
        # SCROLL WHEEL
        # -------------------------

        if event.type == pygame.MOUSEWHEEL:

            if timeline_rect.collidepoint(mx, my):

                self.scroll_x -= event.y * self.scroll_speed
                self.scroll_x = max(self.scroll_x, 0)

        # -------------------------
        # MOUSE DOWN
        # -------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 2 and timeline_rect.collidepoint(mx, my):
                self.drag_scroll = True

            if event.button == 1:

                for i, rect in enumerate(self.frame_rects):

                    if rect.collidepoint(mx, my):

                        self.state.set_frame(i)

                        self.dragging = True
                        self.drag_index = i
                        return

        # -------------------------
        # MOUSE UP
        # -------------------------

        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                self.dragging = False
                self.drag_index = None

            if event.button == 2:

                self.drag_scroll = False

        # -------------------------
        # DRAG TIMELINE
        # -------------------------

        if event.type == pygame.MOUSEMOTION and self.drag_scroll:

            dx = event.rel[0]

            self.scroll_x -= dx
            self.scroll_x = max(self.scroll_x, 0)

        # -------------------------
        # DRAG REORDER
        # -------------------------

        if event.type == pygame.MOUSEMOTION and self.dragging:

            anim = self.state.get_current_animation()

            if not anim:
                return

            mx, my = pygame.mouse.get_pos()

            for i, rect in enumerate(self.frame_rects):

                if rect.collidepoint(mx, my) and i != self.drag_index:

                    anim.frames.insert(
                        i,
                        anim.frames.pop(self.drag_index)
                    )

                    self.drag_index = i
                    self.state.set_frame(i)

                    break

    # -------------------------
    # DRAW
    # -------------------------

    def draw(self, screen):

        layout = self.editor.layout

        timeline_rect = layout.timeline
        frame_preview_rect = layout.frame_editor

        pygame.draw.rect(screen, (35, 35, 35), timeline_rect)
        pygame.draw.rect(screen, (40, 40, 40), frame_preview_rect)

        anim = self.state.get_current_animation()

        if not anim:
            return

        sheet = self.editor.canvas.sheet

        if not sheet:
            return

        # -------------------------
        # TIMELINE FRAMES
        # -------------------------

        total_w = len(anim.frames) * (self.frame_size + self.frame_margin)

        max_scroll = max(0, total_w - timeline_rect.width + 40)
        self.scroll_x = min(self.scroll_x, max_scroll)

        self.frame_rects.clear()

        x = timeline_rect.x + 20 - self.scroll_x
        y = timeline_rect.centery - self.frame_size // 2

        mx, my = pygame.mouse.get_pos()
        self.hover_index = None

        screen.set_clip(timeline_rect)

        for i, frame in enumerate(anim.frames):

            rect = pygame.Rect(
                x,
                y,
                self.frame_size,
                self.frame_size
            )

            self.frame_rects.append(rect)

            if rect.collidepoint(mx, my):
                self.hover_index = i
                pygame.draw.rect(screen, (70, 70, 70), rect)
            else:
                pygame.draw.rect(screen, (50, 50, 50), rect)

            try:

                img = sheet.subsurface(
                    int(frame.x),
                    int(frame.y),
                    int(frame.w),
                    int(frame.h)
                )

                img = pygame.transform.scale(
                    img,
                    (self.frame_size, self.frame_size)
                )

                screen.blit(img, rect)

            except:
                pass

            txt = self.font.render(str(i), True, (200, 200, 200))
            screen.blit(txt, (rect.x + 4, rect.y + 4))

            if self.state.current_frame_index == i:
                pygame.draw.rect(screen, (0, 200, 255), rect, 3)
            else:
                pygame.draw.rect(screen, (90, 90, 90), rect, 1)

            x += self.frame_size + self.frame_margin

        screen.set_clip(None)

        # -------------------------
        # SCROLLBAR
        # -------------------------

        if total_w > timeline_rect.width:

            bar_h = 6
            bar_y = timeline_rect.bottom - bar_h - 4

            visible_ratio = timeline_rect.width / total_w
            bar_w = timeline_rect.width * visible_ratio

            scroll_ratio = self.scroll_x / max_scroll if max_scroll else 0

            bar_x = timeline_rect.x + (timeline_rect.width - bar_w) * scroll_ratio

            pygame.draw.rect(
                screen,
                (80, 80, 80),
                (bar_x, bar_y, bar_w, bar_h)
            )

        # -------------------------
        # FRAME PREVIEW
        # -------------------------

        frame = self.state.get_current_frame()

        if frame and frame.w > 0 and frame.h > 0:

            try:

                img = sheet.subsurface(
                    int(frame.x),
                    int(frame.y),
                    int(frame.w),
                    int(frame.h)
                )

                scale = min(
                    frame_preview_rect.width / frame.w,
                    frame_preview_rect.height / frame.h
                )

                img = pygame.transform.scale(
                    img,
                    (int(frame.w * scale), int(frame.h * scale))
                )

                pos = img.get_rect(center=frame_preview_rect.center)

                screen.blit(img, pos)

            except:
                pass
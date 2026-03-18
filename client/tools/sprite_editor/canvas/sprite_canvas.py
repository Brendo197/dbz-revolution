import pygame
from tools.sprite_editor.canvas.tools.select_tool import SelectTool
from tools.sprite_editor.core.frame import Frame

class SpriteCanvas:

    def __init__(self, editor):

        self.editor = editor
        self.state = editor.state

        self.sheet = None

        self.zoom = 1.0

        self.offset_x = 0
        self.offset_y = 0

        self.dragging = False

        self.start_x = 0
        self.start_y = 0

        self.preview_selection = None

        self.grid = True
        self.grid_size = 32

        self.drag_scroll_x = False
        self.drag_scroll_y = False

        self.h_scroll_rect = pygame.Rect(0, 0, 0, 0)
        self.v_scroll_rect = pygame.Rect(0, 0, 0, 0)

        self.current_tool = SelectTool(self)
        self.sheet_cache = {}
        self.cached_surface = None
        self.cached_zoom = None
        self.hover_slice = None
    # -------------------------
    # LOAD SPRITE SHEET
    # -------------------------


    def add_frame_from_selection(self):

        rect = self.state.selection_rect

        if not rect:
            print("Nenhuma seleção ativa")
            return

        anim = self.state.get_current_animation()

        if not anim:
            print("Nenhuma animação selecionada")
            return

        frame = Frame(rect.x, rect.y, rect.w, rect.h)

        anim.frames.append(frame)

        print("Frame adicionado:", rect)
    def load_sheet(self, path):

        if path in self.sheet_cache:
            self.sheet = self.sheet_cache[path]
        else:
            sheet = pygame.image.load(path).convert_alpha()
            self.sheet_cache[path] = sheet
            self.sheet = sheet

        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0

        # reset cache
        self.cached_surface = None
        self.cached_zoom = None

    def reset(self):

        self.dragging = False
        self.selection_rect = None
    # -------------------------
    # CONVERT SCREEN → CANVAS
    # -------------------------
    def get_scaled_surface(self):

        if not self.sheet:
            return None

        if self.cached_surface and self.cached_zoom == self.zoom:
            return self.cached_surface

        w = int(self.sheet.get_width() * self.zoom)
        h = int(self.sheet.get_height() * self.zoom)

        self.cached_surface = pygame.transform.scale(self.sheet, (w, h))
        self.cached_zoom = self.zoom

        return self.cached_surface
    def screen_to_canvas(self, mx, my):

        canvas_rect = self.editor.layout.canvas

        x = (mx - canvas_rect.x - self.offset_x) / self.zoom
        y = (my - canvas_rect.y - self.offset_y) / self.zoom

        return x, y

    # -------------------------
    # EVENTS
    # -------------------------

    def handle_event(self, event):

        if not self.sheet:
            return
        if self.current_tool:
            self.current_tool.handle_event(event)

        canvas_rect = self.editor.layout.canvas
        mx, my = pygame.mouse.get_pos()

        if canvas_rect.collidepoint(mx, my):
            self.hover_slice = self.get_hovered_selection(mx, my)
        else:
            self.hover_slice = None

        if self.hover_slice:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if event.type != pygame.MOUSEMOTION and not canvas_rect.collidepoint(mx, my):
            return

        # -------------------------
        # MOUSE WHEEL
        # -------------------------

        if event.type == pygame.MOUSEWHEEL:

            keys = pygame.key.get_pressed()

            # ZOOM
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:

                before_x, before_y = self.screen_to_canvas(mx, my)

                old_zoom = self.zoom

                if event.y > 0:
                    self.zoom *= 1.1
                else:
                    self.zoom *= 0.9

                self.zoom = max(0.1, min(self.zoom, 8))

                scale = self.zoom / old_zoom

                self.offset_x = mx - (mx - self.offset_x) * scale
                self.offset_y = my - (my - self.offset_y) * scale

                self.clamp_camera()

                return

            # SCROLL
            else:

                if keys[pygame.K_LSHIFT]:
                    self.offset_x += event.y * 40
                else:
                    self.offset_y += event.y * 40

        # -------------------------
        # MOUSE DOWN
        # -------------------------
        # -------------------------
        # RIGHT CLICK → REMOVE SELECTION
        # -------------------------

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:

            mx, my = pygame.mouse.get_pos()
            canvas_rect = self.editor.layout.canvas

            if not canvas_rect.collidepoint(mx, my):
                return

            hover = self.hover_slice

            if hover:

                # remove da lista principal
                if hover in self.state.selections:
                    self.state.selections.remove(hover)

                # remove preview também
                if hover in self.state.slice_previews:
                    self.state.slice_previews.remove(hover)

                # limpa seleção ativa
                if self.state.selection_rect == hover:
                    self.state.selection_rect = None

                print("Seleção removida:", hover)

                return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if canvas_rect.collidepoint(mx, my):

                hover = self.hover_slice

                # clicou em uma seleção existente
                if hover:
                    self.state.selection_rect = hover
                    self.add_frame_from_selection()

                    return

                # iniciar nova seleção
                self.start_x, self.start_y = self.screen_to_canvas(mx, my)

                self.dragging = True
                self.preview_selection = None
                self.state.slice_previews.clear()

                return

                # iniciar seleção
                self.start_x, self.start_y = self.screen_to_canvas(mx, my)

                self.dragging = True
                self.preview_selection = None
                self.state.slice_previews.clear()

                return
        # -------------------------
        # MOUSE UP
        # -------------------------

        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1 and self.dragging:

                x, y = self.screen_to_canvas(mx, my)

                x1 = min(self.start_x, x)
                y1 = min(self.start_y, y)

                x2 = max(self.start_x, x)
                y2 = max(self.start_y, y)

                w = x2 - x1
                h = y2 - y1

                if w > 2 and h > 2:

                    self.state.selection_rect = pygame.Rect(x1, y1, w, h)

                    print("FRAME:", self.state.selection_rect)

                self.preview_selection = None
                self.dragging = False
                self.drag_scroll_x = False
                self.drag_scroll_y = False

        # -------------------------
        # MOUSE MOVE
        # -------------------------

        if event.type == pygame.MOUSEMOTION:

            # PAN COM BOTAO DO MEIO
            if pygame.mouse.get_pressed()[1]:

                dx, dy = event.rel

                self.offset_x += dx
                self.offset_y += dy

            if self.drag_scroll_x:
                dx = event.rel[0]
                self.offset_x -= dx * (self.sheet.get_width() * self.zoom / canvas_rect.width)

            if self.drag_scroll_y:
                dy = event.rel[1]
                self.offset_y -= dy * (self.sheet.get_height() * self.zoom / canvas_rect.height)

            # PREVIEW SELECTION
            if self.dragging:

                x, y = self.screen_to_canvas(mx, my)

                x1 = min(self.start_x, x)
                y1 = min(self.start_y, y)

                x2 = max(self.start_x, x)
                y2 = max(self.start_y, y)

                self.preview_selection = (x1, y1, x2 - x1, y2 - y1)

        self.clamp_camera()

    # -------------------------
    # GRID
    # -------------------------

    def draw_grid(self, screen, canvas_rect):

        if not self.grid or not self.sheet:
            return

        w = int(self.sheet.get_width() * self.zoom)
        h = int(self.sheet.get_height() * self.zoom)

        size = int(self.grid_size * self.zoom)

        start_x = int(-self.offset_x // size) * size
        end_x = start_x + canvas_rect.width + size

        for x in range(start_x, end_x, size):

            pygame.draw.line(
                screen,
                (60, 60, 60),
                (canvas_rect.x + x + self.offset_x, canvas_rect.y + self.offset_y),
                (canvas_rect.x + x + self.offset_x, canvas_rect.y + h + self.offset_y),
            )

        for y in range(0, h, size):

            pygame.draw.line(
                screen,
                (60, 60, 60),
                (canvas_rect.x + self.offset_x, canvas_rect.y + y + self.offset_y),
                (canvas_rect.x + w + self.offset_x, canvas_rect.y + y + self.offset_y),
            )

    # -------------------------
    # DRAW
    # -------------------------

    def draw(self, screen):

        if not self.sheet:
            return

        canvas_rect = self.editor.layout.canvas

        pygame.draw.rect(screen, (25, 25, 25), canvas_rect)

        surface = self.get_scaled_surface()

        if surface is None:
            return

        old_clip = screen.get_clip()
        screen.set_clip(canvas_rect)

        screen.blit(
            surface,
            (
                canvas_rect.x + self.offset_x,
                canvas_rect.y + self.offset_y
            )
        )

        self.draw_grid(screen, canvas_rect)

        if self.preview_selection:
            x, y, w, h = self.preview_selection

            x = int(canvas_rect.x + x * self.zoom + self.offset_x)
            y = int(canvas_rect.y + y * self.zoom + self.offset_y)

            w = int(w * self.zoom)
            h = int(h * self.zoom)

            pygame.draw.rect(screen, (255, 255, 0), (x, y, w, h), 1)

        if self.current_tool:
            self.current_tool.draw(screen)


        mx, my = pygame.mouse.get_pos()
        hover = self.hover_slice

        for rect in self.state.slice_previews:

            x = int(canvas_rect.x + rect.x * self.zoom + self.offset_x)
            y = int(canvas_rect.y + rect.y * self.zoom + self.offset_y)

            w = int(rect.w * self.zoom)
            h = int(rect.h * self.zoom)

            key = (rect.x, rect.y, rect.w, rect.h)

            if key in self.state.animation_frames:
                color = (0, 120, 255)  # azul
            else:
                color = (255, 220, 0)  # amarelo

            if rect == hover:
                if key in self.state.animation_frames:
                    color = (120, 180, 255)
                else:
                    color = (255, 240, 120)

            pygame.draw.rect(screen, color, (x, y, w, h), 2)

        for rect in self.state.selections:
            x = int(canvas_rect.x + rect.x * self.zoom + self.offset_x)
            y = int(canvas_rect.y + rect.y * self.zoom + self.offset_y)

            w = int(rect.w * self.zoom)
            h = int(rect.h * self.zoom)

            pygame.draw.rect(screen, (0, 255, 255), (x, y, w, h), 2)

        screen.set_clip(old_clip)

        self.draw_scrollbars(screen)
    # -------------------------
    # LIMIT CAMERA
    # -------------------------

    def clamp_camera(self):

        if not self.sheet:
            return

        canvas = self.editor.layout.canvas

        sheet_w = self.sheet.get_width() * self.zoom
        sheet_h = self.sheet.get_height() * self.zoom

        min_x = min(0, canvas.width - sheet_w)
        min_y = min(0, canvas.height - sheet_h)

        self.offset_x = max(min(self.offset_x, 0), min_x)
        self.offset_y = max(min(self.offset_y, 0), min_y)

    # -------------------------
    # SCROLLBARS
    # -------------------------

    def draw_scrollbars(self, screen):

        canvas = self.editor.layout.canvas

        sheet_w = self.sheet.get_width() * self.zoom
        sheet_h = self.sheet.get_height() * self.zoom

        if sheet_w <= 0 or sheet_h <= 0:
            return

        view_ratio_x = canvas.width / sheet_w
        bar_w = canvas.width * view_ratio_x

        pos_x = (-self.offset_x / sheet_w) * canvas.width

        view_ratio_y = canvas.height / sheet_h
        bar_h = canvas.height * view_ratio_y

        bar_w = max(30, min(canvas.width, bar_w))
        bar_h = max(30, min(canvas.height, bar_h))

        pos_y = (-self.offset_y / sheet_h) * canvas.height
        pos_x = max(0, min(canvas.width - bar_w, pos_x))
        pos_y = max(0, min(canvas.height - bar_h, pos_y))
        pygame.draw.rect(
            screen,
            (90, 90, 90),
            (
                canvas.x + pos_x,
                canvas.bottom - 8,
                bar_w,
                6
            )
        )

        pygame.draw.rect(
            screen,
            (90, 90, 90),
            (
                canvas.right - 8,
                canvas.y + pos_y,
                6,
                bar_h
            )
        )

        self.h_scroll_rect = pygame.Rect(
            canvas.x + pos_x,
            canvas.bottom - 8,
            bar_w,
            6
        )

        self.v_scroll_rect = pygame.Rect(
            canvas.right - 8,
            canvas.y + pos_y,
            6,
            bar_h
        )

    def get_hovered_selection(self, mx, my):

        x, y = self.screen_to_canvas(mx, my)

        for rect in reversed(self.state.selections):

            if rect.collidepoint(x, y):
                return rect

        return None
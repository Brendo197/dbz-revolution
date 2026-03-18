import pygame


class Layout:

    def __init__(self, editor):

        self.editor = editor
        self.update()

    def update(self):

        w, h = self.editor.screen.get_size()

        toolbar_h = self.editor.toolbar.height

        left_w = 220
        right_w = 260
        timeline_h = 160

        center_w = w - left_w - right_w

        # -------------------------
        # LEFT PANEL
        # -------------------------

        left_h = h - toolbar_h - timeline_h
        half_left = left_h // 2

        self.sprite_list = pygame.Rect(
            0,
            toolbar_h,
            left_w,
            half_left
        )

        self.animation_list = pygame.Rect(
            0,
            toolbar_h + half_left,
            left_w,
            left_h - half_left
        )

        # -------------------------
        # RIGHT PANEL
        # -------------------------

        self.right_panel = pygame.Rect(
            w - right_w,
            toolbar_h,
            right_w,
            h - toolbar_h - timeline_h
        )

        # -------------------------
        # CANVAS
        # -------------------------

        self.canvas = pygame.Rect(
            left_w,
            toolbar_h,
            center_w,
            h - toolbar_h - timeline_h
        )

        # -------------------------
        # BOTTOM AREA
        # -------------------------

        bottom_y = h - timeline_h

        # preview da animação
        self.preview = pygame.Rect(
            0,
            bottom_y,
            left_w,
            timeline_h
        )

        # timeline
        self.timeline = pygame.Rect(
            left_w,
            bottom_y,
            center_w,
            timeline_h
        )

        # frame preview
        self.frame_editor = pygame.Rect(
            w - right_w,
            bottom_y,
            right_w,
            timeline_h
        )

    # -------------------------
    # DEBUG DRAW
    # -------------------------

    def draw(self, screen):

        pygame.draw.rect(screen, (50,50,50), self.sprite_list)
        pygame.draw.rect(screen, (55,55,55), self.animation_list)

        pygame.draw.rect(screen, (20,20,20), self.canvas)

        pygame.draw.rect(screen, (40,40,40), self.timeline)
        pygame.draw.line(screen, (70,70,70), self.timeline.topleft, self.timeline.topright)

        pygame.draw.rect(screen, (45,45,45), self.right_panel)

        pygame.draw.rect(screen, (35,35,35), self.preview)
        pygame.draw.rect(screen, (35,35,35), self.frame_editor)
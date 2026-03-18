import pygame


class FrameList:

    def __init__(self, editor):

        self.editor = editor

        self.x = 0
        self.y = 0
        self.width = 200
        self.height = 400

        self.frame_size = 64
        self.padding = 6


    def update_layout(self):

        layout = self.editor.layout

        self.x = layout.left_panel_x
        self.y = layout.frames_y

        self.width = layout.left_panel_w
        self.height = layout.frames_h


    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = event.pos

            if not self._inside(mx, my):
                return

            index = self._frame_at(mx, my)

            sprite = self.editor.state.get_current_sprite()

            if not sprite:
                return

            anim = self.editor.state.get_current_animation()

            if not anim:
                return

            if index < len(anim.frames):
                self.editor.state.set_frame(index)

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (25, 25, 25),
            (self.x, self.y, self.width, self.height)
        )
        sprite = self.editor.state.get_current_sprite()

        if not sprite:
            return

        anim = self.editor.state.get_current_animation()

        if not anim:
            return

        frames = anim.frames

        sheet = self.editor.canvas.sheet

        cols = max(1, self.width // (self.frame_size + self.padding))

        for i, frame in enumerate(frames):
            col = i % cols
            row = i // cols

            x = self.x + col * (self.frame_size + self.padding)
            y = self.y + row * (self.frame_size + self.padding)

            rect = pygame.Rect(frame.x, frame.y, frame.w, frame.h)

            if rect.right > sheet.get_width() or rect.bottom > sheet.get_height():
                continue

            img = sheet.subsurface(rect)
            sheet = self.editor.canvas.sheet

            if not sheet:
                return
            img = pygame.transform.scale(img, (self.frame_size, self.frame_size))
            selected = self.editor.state.current_frame_index == i
            screen.blit(img, (x, y))

            if selected:
                pygame.draw.rect(
                    screen,
                    (0, 255, 255),
                    (x - 2, y - 2, self.frame_size + 4, self.frame_size + 4),
                    2
                )

    def _frame_at(self, mx, my):

        cols = max(1, self.width // (self.frame_size + self.padding))

        local_x = mx - self.x
        local_y = my - self.y

        col = local_x // (self.frame_size + self.padding)
        row = local_y // (self.frame_size + self.padding)

        return int(row * cols + col)


    def _inside(self, x, y):

        return (
            self.x <= x <= self.x + self.width
            and self.y <= y <= self.y + self.height
        )
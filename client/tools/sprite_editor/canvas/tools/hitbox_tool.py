import pygame
from tools.sprite_editor.core.hitbox import Hitbox


class HitboxTool:

    def __init__(self, canvas):

        self.canvas = canvas

        self.dragging = False

        self.start_x = 0
        self.start_y = 0

        self.preview = None

    def handle_event(self, event):

        state = self.canvas.state
        frame = state.get_current_frame()

        if not frame:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            mx, my = pygame.mouse.get_pos()

            x, y = self.canvas.screen_to_canvas(mx, my)

            self.start_x = x
            self.start_y = y

            self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:

            mx, my = pygame.mouse.get_pos()

            x, y = self.canvas.screen_to_canvas(mx, my)

            x1 = min(self.start_x, x)
            y1 = min(self.start_y, y)

            x2 = max(self.start_x, x)
            y2 = max(self.start_y, y)

            w = x2 - x1
            h = y2 - y1

            hitbox = Hitbox(x1, y1, w, h)

            frame.hitboxes.append(hitbox)

            self.dragging = False
            self.preview = None

        elif event.type == pygame.MOUSEMOTION and self.dragging:

            mx, my = pygame.mouse.get_pos()

            x, y = self.canvas.screen_to_canvas(mx, my)

            x1 = min(self.start_x, x)
            y1 = min(self.start_y, y)

            x2 = max(self.start_x, x)
            y2 = max(self.start_y, y)

            self.preview = (x1, y1, x2 - x1, y2 - y1)
import pygame


class MoveTool:

    def __init__(self, canvas):

        self.canvas = canvas
        self.state = canvas.state

        self.drag_rect = None

        self.offset_x = 0
        self.offset_y = 0

        self.dragging = False

    # -----------------------------------------
    # EVENTS
    # -----------------------------------------

    def handle_event(self, event):

        mx, my = pygame.mouse.get_pos()

        x, y = self.canvas.screen_to_canvas(mx, my)

        # -------------------------
        # CLICK
        # -------------------------

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            hovered = None

            for rect in reversed(self.state.selections):

                if rect.collidepoint(x, y):
                    hovered = rect
                    break

            if hovered:

                self.drag_rect = hovered

                self.offset_x = x - hovered.x
                self.offset_y = y - hovered.y

                self.dragging = True

        # -------------------------
        # MOVE
        # -------------------------

        elif event.type == pygame.MOUSEMOTION:

            if self.dragging and self.drag_rect:

                new_x = x - self.offset_x
                new_y = y - self.offset_y

                # limitar dentro da sprite sheet
                if self.canvas.sheet:

                    max_x = self.canvas.sheet.get_width() - self.drag_rect.w
                    max_y = self.canvas.sheet.get_height() - self.drag_rect.h

                    new_x = max(0, min(new_x, max_x))
                    new_y = max(0, min(new_y, max_y))

                self.drag_rect.x = new_x
                self.drag_rect.y = new_y

        # -------------------------
        # RELEASE
        # -------------------------

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

            self.drag_rect = None
            self.dragging = False

    # -----------------------------------------
    # DRAW
    # -----------------------------------------

    def draw(self, screen):
        pass
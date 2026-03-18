import pygame
from tools.sprite_editor.core.auto_slice import detect_slices


class SliceTool:

    def __init__(self, canvas):

        self.canvas = canvas
        self.state = canvas.state

        self.dragging = False

        self.start_x = 0
        self.start_y = 0

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    def handle_event(self, event):

        canvas = self.canvas

        mx, my = pygame.mouse.get_pos()

        # --------------------------------
        # START DRAG
        # --------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            self.start_x, self.start_y = canvas.screen_to_canvas(mx, my)

            self.dragging = True
            canvas.preview_selection = None

        # --------------------------------
        # DRAGGING
        # --------------------------------

        elif event.type == pygame.MOUSEMOTION and self.dragging:

            x, y = canvas.screen_to_canvas(mx, my)

            x1 = min(self.start_x, x)
            y1 = min(self.start_y, y)

            w = abs(x - self.start_x)
            h = abs(y - self.start_y)

            canvas.preview_selection = (x1, y1, w, h)

        # --------------------------------
        # RELEASE
        # --------------------------------

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

            if canvas.preview_selection:

                x, y, w, h = canvas.preview_selection

                rect = pygame.Rect(x, y, w, h)

                surface = canvas.sheet

                slices = detect_slices(surface, rect)

                for s in slices:

                    # evita duplicar
                    exists = False

                    for r in self.state.selections:

                        if r == s:
                            exists = True
                            break

                    if not exists:
                        self.state.selections.append(s)

            self.dragging = False
            canvas.preview_selection = None

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    def draw(self, screen):

        # o preview já é desenhado pelo canvas
        pass
import pygame

class SelectTool:

    def __init__(self, canvas):
        self.canvas = canvas
        self.state = canvas.state

    def handle_event(self, event):

        canvas = self.canvas
        mx, my = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            canvas.start_x, canvas.start_y = canvas.screen_to_canvas(mx, my)
            canvas.dragging = True
            canvas.preview_selection = None

        elif event.type == pygame.MOUSEMOTION and canvas.dragging:

            x, y = canvas.screen_to_canvas(mx, my)

            x1 = min(canvas.start_x, x)
            y1 = min(canvas.start_y, y)

            w = abs(x - canvas.start_x)
            h = abs(y - canvas.start_y)

            canvas.preview_selection = (x1, y1, w, h)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:

            if canvas.preview_selection:

                x, y, w, h = canvas.preview_selection

                rect = pygame.Rect(x, y, w, h)

                self.state.selections.append(rect)

            canvas.dragging = False
            canvas.preview_selection = None
    def draw(self,canvas):

        pass
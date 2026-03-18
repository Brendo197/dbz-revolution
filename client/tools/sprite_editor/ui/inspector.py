import pygame


class Inspector:

    def __init__(self, editor):

        self.editor = editor
        self.state = editor.state

        self.font = pygame.font.SysFont("arial", 14)

        self.active_tab = "frame"

        self.tab_frame = pygame.Rect(0, 0, 0, 0)
        self.tab_anim = pygame.Rect(0, 0, 0, 0)

        self.inputs = {}
        self.active_input = None

        self.last_frame = None
        self.last_anim = None


    # -------------------------
    # EVENTOS
    # -------------------------

    def handle_event(self, event):

        mx, my = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.tab_frame.collidepoint(mx, my):
                self.active_tab = "frame"
                self.reset_inputs()
                return

            if self.tab_anim.collidepoint(mx, my):
                self.active_tab = "anim"
                self.reset_inputs()
                return

            clicked_input = None

            for key, data in self.inputs.items():

                if data["rect"].collidepoint(mx, my):

                    if data["type"] == "checkbox":
                        self.toggle_checkbox(key)
                        return

                    clicked_input = key
                    break

            # aplicamos o valor do input anterior
            if self.active_input and self.active_input != clicked_input:
                self.apply_input(self.active_input)

            self.active_input = clicked_input


        if event.type == pygame.KEYDOWN and self.active_input:

            field = self.active_input

            if event.key == pygame.K_BACKSPACE:

                self.inputs[field]["text"] = self.inputs[field]["text"][:-1]

            elif event.key == pygame.K_RETURN:

                self.apply_input(field)
                self.active_input = None

            else:

                if event.unicode.isdigit() or event.unicode == "-":
                    self.inputs[field]["text"] += event.unicode


    # -------------------------
    # RESET INPUTS
    # -------------------------

    def reset_inputs(self):

        self.inputs.clear()
        self.active_input = None


    # -------------------------
    # APLICAR INPUT
    # -------------------------

    def apply_input(self, field):

        frame = self.state.get_current_frame()
        anim = self.state.get_current_animation()

        text = self.inputs[field]["text"]

        try:
            value = int(text)
        except:
            return

        if self.active_tab == "frame" and frame:

            if field == "tick_override":

                frame.tick_override = None if value == 0 else value

            else:

                setattr(frame, field, value)

        elif self.active_tab == "anim" and anim:

            setattr(anim, field, value)

        print("[INSPECTOR] atualizado:", field, value)


    # -------------------------
    # CHECKBOX
    # -------------------------

    def toggle_checkbox(self, field):

        frame = self.state.get_current_frame()
        anim = self.state.get_current_animation()

        if self.active_tab == "frame" and frame:

            value = getattr(frame, field)
            setattr(frame, field, not value)

        elif self.active_tab == "anim" and anim:

            value = getattr(anim, field)
            setattr(anim, field, not value)

        print("[INSPECTOR] checkbox:", field)


    # -------------------------
    # DRAW
    # -------------------------

    def draw(self, screen):

        layout = self.editor.layout
        rect = layout.right_panel

        pygame.draw.rect(screen, (45, 45, 45), rect)

        self.draw_tabs(screen, rect)

        frame = self.state.get_current_frame()
        anim = self.state.get_current_animation()

        if frame != self.last_frame or anim != self.last_anim:
            self.reset_inputs()
            self.last_frame = frame
            self.last_anim = anim

        if self.active_tab == "frame":
            self.draw_frame(screen, rect)
        else:
            self.draw_anim(screen, rect)


    # -------------------------
    # TABS
    # -------------------------

    def draw_tabs(self, screen, rect):

        h = 28

        self.tab_frame = pygame.Rect(rect.x, rect.y, rect.width // 2, h)
        self.tab_anim = pygame.Rect(rect.centerx, rect.y, rect.width // 2, h)

        c1 = (70, 70, 70) if self.active_tab == "frame" else (55, 55, 55)
        c2 = (70, 70, 70) if self.active_tab == "anim" else (55, 55, 55)

        pygame.draw.rect(screen, c1, self.tab_frame)
        pygame.draw.rect(screen, c2, self.tab_anim)

        screen.blit(self.font.render("Frame", True, (255, 255, 255)),
                    (self.tab_frame.x + 8, self.tab_frame.y + 6))

        screen.blit(self.font.render("Animation", True, (255, 255, 255)),
                    (self.tab_anim.x + 8, self.tab_anim.y + 6))


    # -------------------------
    # INPUT
    # -------------------------

    def input(self, screen, label, value, x, y, w, field):

        screen.blit(self.font.render(label, True, (220, 220, 220)), (x, y))

        rect = pygame.Rect(x, y + 18, w, 22)

        pygame.draw.rect(screen, (60, 60, 60), rect)
        pygame.draw.rect(screen, (90, 90, 90), rect, 1)

        if field not in self.inputs:
            self.inputs[field] = {"text": str(value)}

        text = self.inputs[field]["text"]

        screen.blit(self.font.render(text, True, (255, 255, 255)),
                    (rect.x + 4, rect.y + 3))

        self.inputs[field]["rect"] = rect
        self.inputs[field]["type"] = "input"


    # -------------------------
    # CHECKBOX
    # -------------------------

    def checkbox(self, screen, label, value, x, y, field):

        rect = pygame.Rect(x, y, 18, 18)

        pygame.draw.rect(screen, (60, 60, 60), rect)
        pygame.draw.rect(screen, (90, 90, 90), rect, 1)

        if value:

            pygame.draw.line(screen, (0, 200, 255),
                             (rect.x + 3, rect.y + 9),
                             (rect.x + 8, rect.y + 14), 2)

            pygame.draw.line(screen, (0, 200, 255),
                             (rect.x + 8, rect.y + 14),
                             (rect.x + 15, rect.y + 3), 2)

        screen.blit(self.font.render(label, True, (220, 220, 220)),
                    (rect.right + 6, rect.y))

        self.inputs[field] = {
            "rect": rect,
            "type": "checkbox"
        }


    # -------------------------
    # FRAME
    # -------------------------

    def draw_frame(self, screen, rect):

        frame = self.state.get_current_frame()

        if not frame:
            return

        x = rect.x + 10
        y = rect.y + 40
        w = rect.width - 20

        self.input(screen, "Origin X", frame.origin_x, x, y, w, "origin_x")
        y += 45

        self.input(screen, "Origin Y", frame.origin_y, x, y, w, "origin_y")
        y += 45

        self.input(screen, "Offset X", frame.offset_x, x, y, w, "offset_x")
        y += 45

        self.input(screen, "Offset Y", frame.offset_y, x, y, w, "offset_y")
        y += 45

        tick = frame.tick_override if frame.tick_override else 0
        self.input(screen, "Tick Override", tick, x, y, w, "tick_override")
        y += 45

        self.checkbox(screen, "Attack Frame", frame.attack_frame, x, y, "attack_frame")


    # -------------------------
    # ANIMATION
    # -------------------------

    def draw_anim(self, screen, rect):

        anim = self.state.get_current_animation()

        if not anim:
            return

        x = rect.x + 10
        y = rect.y + 40
        w = rect.width - 20

        self.input(screen, "Tick", anim.tick, x, y, w, "tick")
        y += 45

        self.checkbox(screen, "Loop", anim.loop, x, y, "loop")
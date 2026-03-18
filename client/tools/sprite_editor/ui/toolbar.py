import pygame

from tools.sprite_editor.canvas.tools.select_tool import SelectTool
from tools.sprite_editor.canvas.tools.move_tool import MoveTool
from tools.sprite_editor.canvas.tools.slice_tool import SliceTool


class Toolbar:

    def __init__(self, editor):

        self.editor = editor
        self.height = 40
        self.buttons = []

        self.active_tool = "select"

        self.create_buttons()

    # --------------------------------------------------
    # BUTTON SETUP
    # --------------------------------------------------

    def create_buttons(self):

        x = 10
        y = 5

        def add(name, action):
            nonlocal x

            rect = pygame.Rect(x, y, 110, 30)

            self.buttons.append({
                "name": name,
                "rect": rect,
                "action": action
            })

            x += 120

        add("New Sprite", self.new_sprite)
        add("Save", self.save_sprite)
        add("Load Sheet", self.load_sheet)
        add("Grid", self.toggle_grid)

        add("Select", self.tool_select)
        add("Move", self.tool_move)
        add("Slice", self.tool_slice)

    # --------------------------------------------------
    # BUTTON ACTIONS
    # --------------------------------------------------

    def new_sprite(self):

        print("NEW SPRITE")

        from network.sender import create_sprite

        create_sprite(self.editor.client_socket)

    def save_sprite(self):

        print("SAVE SPRITE")

        from network.sender import send_save_sprite_project

        project = self.editor.state.project

        if project:
            send_save_sprite_project(self.editor.client_socket, project)

    def load_sheet(self):

        print("LOAD SHEET")

        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()

        path = filedialog.askopenfilename()

        if path:
            self.editor.canvas.load_sheet(path)

    def toggle_grid(self):

        canvas = self.editor.canvas
        canvas.grid = not canvas.grid

    # --------------------------------------------------
    # TOOL ACTIONS
    # --------------------------------------------------

    def tool_select(self):

        self.active_tool = "select"

        self.editor.canvas.current_tool = SelectTool(self.editor.canvas)

    def tool_move(self):

        self.active_tool = "move"

        self.editor.canvas.current_tool = MoveTool(self.editor.canvas)

    def tool_slice(self):

        self.active_tool = "slice"

        self.editor.canvas.current_tool = SliceTool(self.editor.canvas)

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            mx, my = pygame.mouse.get_pos()

            for b in self.buttons:

                if b["rect"].collidepoint(mx, my):

                    action = b["action"]
                    action()

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    def draw(self, screen):

        # background
        pygame.draw.rect(
            screen,
            (45, 45, 45),
            (0, 0, screen.get_width(), self.height)
        )

        font = pygame.font.SysFont("arial", 16)

        for b in self.buttons:

            name = b["name"].lower()

            color = (70, 70, 70)

            # highlight tool active
            if name == self.active_tool:
                color = (110, 110, 110)

            pygame.draw.rect(screen, color, b["rect"])

            text = font.render(b["name"], True, (220, 220, 220))

            screen.blit(
                text,
                (b["rect"].x + 10, b["rect"].y + 6)
            )
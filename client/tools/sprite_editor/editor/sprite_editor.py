import pygame
import os
from game.session import session
from tools.sprite_editor.ui.sprite_list import SpriteList
from tools.sprite_editor.ui.animation_list import AnimationList
from tools.sprite_editor.ui.layout import Layout
from tools.sprite_editor.canvas.sprite_canvas import SpriteCanvas
from tools.sprite_editor.ui.toolbar import Toolbar
from tools.sprite_editor.ui.timeline import Timeline
from tools.sprite_editor.editor.editor_state import EditorState
from tools.sprite_editor.core.auto_slice import detect_slices
from tools.sprite_editor.ui.frame_list import FrameList
from tools.sprite_editor.ui.inspector import Inspector
from tools.sprite_editor.editor.animation_preview import AnimationPreview

SPRITE_FOLDER = os.path.join("assets", "sprites")


class SpriteEditor:

    def __init__(self, client_socket=None):

        pygame.init()

        info = pygame.display.Info()
        self.client_socket = client_socket
        width = int(info.current_w * 0.8)
        height = int(info.current_h * 0.8)

        self.screen = pygame.display.set_mode(
            (width, height),
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Sprite Editor")

        self.clock = pygame.time.Clock()

        # STATE DO EDITOR
        self.state = EditorState()

        self.toolbar = Toolbar(self)
        # layout precisa da screen
        self.layout = Layout(self)

        self.canvas = SpriteCanvas(self)
        self.preview = AnimationPreview(self)
        # TIMELINE
        self.timeline = Timeline(self)
        self.inspector = Inspector(self)
        self.sprite_list = SpriteList(self)
        self.animation_list = AnimationList(self)
        self.selected_sprite_id = None
        # self.frame_list = FrameList(self)
        self.clock = pygame.time.Clock()
        self.delta = 0
        from network.sender import request_sprite_list
        request_sprite_list(client_socket)
        self.run()

    def load_first_sprite(self):

        if not os.path.exists(SPRITE_FOLDER):
            print("Pasta de sprites não encontrada")
            return

        sprites = []

        for file in os.listdir(SPRITE_FOLDER):

            if file.endswith(".png"):

                sprite_id = int(file.replace(".png", ""))

                sprites.append(sprite_id)

        print("Sprites encontrados:", sprites)

        if sprites:

            sheet_path = os.path.join(SPRITE_FOLDER, f"{sprites[0]}.png")

            self.canvas.load_sheet(sheet_path)

    def run(self):

        running = True

        while running:
            self.delta = self.clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_DELETE:

                        anim = self.state.get_current_animation()
                        idx = self.state.current_frame_index

                        if not anim or not anim.frames or idx is None:
                            continue

                        # evita apagar último frame
                        if len(anim.frames) <= 1:
                            print("Não é possível deletar o último frame")
                            continue

                        import tkinter as tk
                        from tkinter import messagebox

                        root = tk.Tk()
                        root.withdraw()

                        confirm = messagebox.askyesno(
                            "Remover Frame",
                            f"Deseja apagar o frame {idx}?"
                        )

                        root.destroy()

                        if confirm:

                            del anim.frames[idx]

                            # ajuste do índice
                            if len(anim.frames) == 0:
                                self.state.current_frame_index = None
                            else:
                                self.state.current_frame_index = max(
                                    0,
                                    min(idx, len(anim.frames) - 1)
                                )

                            # sincroniza preview
                            self.preview.player.set_frame(
                                self.state.current_frame_index or 0
                            )
                if event.type == pygame.VIDEORESIZE:

                    self.screen = pygame.display.set_mode(
                        (event.w, event.h),
                        pygame.RESIZABLE
                    )

                    self.layout.update()

                elif event.type == pygame.WINDOWRESIZED:

                    self.layout.update()


                self.toolbar.handle_event(event)
                self.preview.handle_event(event)
                self.timeline.handle_event(event)
                if not self.preview.fullscreen:
                    self.canvas.handle_event(event)
                self.sprite_list.handle_event(event)
                self.animation_list.handle_event(event)
                self.inspector.handle_event(event)

                if session.sprite_project_updated:

                    project = session.sprite_project

                    self.state.set_project(project)

                    # carregar primeira animação automaticamente
                    if project.animations:

                        # suporta dict ou lista
                        if isinstance(project.animations, dict):
                            animations = list(project.animations.values())
                        else:
                            animations = list(project.animations)

                        if len(animations) > 0:

                            first_anim = animations[0]

                            print("AUTO SELECT ANIM:", first_anim.name)

                            self.state.set_animation(first_anim.name)

                            # força reset consistente
                            if first_anim.frames:
                                self.state.set_frame(0)
                            else:
                                self.state.current_frame_index = None

                            # 🔥 sincroniza preview
                            self.preview.player.play(first_anim)
                            self.preview.player.set_frame(0)

                    # carregar sprite sheet automaticamente
                    if project.id:

                        sheet_path = os.path.join(SPRITE_FOLDER, f"{project.id}.png")

                        if os.path.exists(sheet_path):
                            self.canvas.load_sheet(sheet_path)
                        else:
                            print("Sprite sheet não encontrada:", sheet_path)

                    session.sprite_project_updated = False
            self.preview.update(self.delta)
            self.screen.fill((30, 30, 30))

            self.layout.draw(self.screen)

            self.sprite_list.draw(self.screen)
            self.animation_list.draw(self.screen)

            self.inspector.draw(self.screen)

            if not self.preview.fullscreen:
                self.canvas.draw(self.screen)

            self.timeline.draw(self.screen)

            self.toolbar.draw(self.screen)
            self.preview.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

    def update(self):

        w, h = self.screen.get_size()

        self.left_panel = pygame.Rect(0, 0, 260, h)

        self.right_panel = pygame.Rect(w - 260, 0, 260, h)
        self.frame_list.update_layout()
        self.timeline = pygame.Rect(
            260,
            h - 160,
            w - 520,
            160
        )

        self.canvas = pygame.Rect(
            260,
            0,
            w - 520,
            h - 160
        )

    def run_slice_preview(self):

        selection = self.state.selection_rect

        if not selection:
            return

        surface = self.canvas.sheet

        slices = detect_slices(surface, selection)

        for rect in slices:

            if rect not in self.state.selections:
                self.state.selections.append(rect)
        self.state.slice_previews.clear()
        self.state.slice_previews.extend(slices)

    def load(self):

        from io.sprite_loader import load_project

        self.project = load_project("sprite.json")

    def save(self):

        from network.sender import send_save_sprite_project

        project = self.state.project

        if project and self.client_socket:
            print("[EDITOR] Sending sprite project to server")

            send_save_sprite_project(self.client_socket, project)
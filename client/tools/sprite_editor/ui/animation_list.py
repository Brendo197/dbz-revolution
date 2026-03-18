import pygame
import tkinter as tk
from tkinter import simpledialog, messagebox


class AnimationList:

    def __init__(self, editor):

        self.editor = editor
        self.state = editor.state

        self.items = []
        self.rects = []

        self.add_rect = pygame.Rect(0, 0, 0, 0)

        self.scroll = 0
        self.max_scroll = 0

        self.font = pygame.font.SysFont("arial", 15)

        # contexto
        self.context_menu = None  # (x, y, index)

        # drag
        self.dragging = False
        self.drag_index = None

    # ------------------------------------------------
    # EVENTS
    # ------------------------------------------------

    def handle_event(self, event):

        mx, my = pygame.mouse.get_pos()
        rect = self.editor.layout.animation_list
        project = self.state.project

        if not project:
            return

        # 🔥 garante lista de ordem
        if not hasattr(project, "animation_order"):
            project.animation_order = list(project.animations.keys())

        order = project.animation_order

        # -------------------------
        # CONTEXT MENU CLICK
        # -------------------------
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.context_menu:

                x, y, index = self.context_menu

                for i, opt in enumerate(["Rename", "Delete"]):

                    r = pygame.Rect(x, y + i * 25, 120, 25)

                    if r.collidepoint(mx, my):

                        if opt == "Rename":
                            self.rename_current()

                        elif opt == "Delete":
                            self.delete_current()

                        self.context_menu = None
                        return

                self.context_menu = None

        # -------------------------
        # SCROLL
        # -------------------------
        if event.type == pygame.MOUSEWHEEL and rect.collidepoint(mx, my):

            self.scroll -= event.y * 20
            self.scroll = max(0, min(self.scroll, self.max_scroll))

        # -------------------------
        # MOUSE DOWN
        # -------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:

            # botão direito → menu
            if event.button == 3:

                for i, r in enumerate(self.rects):
                    if r.collidepoint(mx, my):
                        self.context_menu = (mx, my, i)
                        return

            # botão esquerdo
            if event.button == 1:

                for i, r in enumerate(self.rects):

                    if r.collidepoint(mx, my):

                        # 🔥 inicia drag
                        self.dragging = True
                        self.drag_index = i

                        name = order[i]
                        self.state.set_animation(name)

                        anim = self.state.get_current_animation()
                        if anim:
                            self.editor.preview.player.play(anim)
                            self.editor.preview.player.set_frame(0)

                        return

                # botão add
                if self.add_rect.collidepoint(mx, my):
                    self.create_animation()
                    return

                self.context_menu = None

        # -------------------------
        # DRAG
        # -------------------------
        if event.type == pygame.MOUSEMOTION and self.dragging:

            for i, r in enumerate(self.rects):

                if r.collidepoint(mx, my) and i != self.drag_index:

                    order.insert(i, order.pop(self.drag_index))
                    self.drag_index = i
                    break

        # -------------------------
        # MOUSE UP
        # -------------------------
        if event.type == pygame.MOUSEBUTTONUP:

            self.dragging = False
            self.drag_index = None

        # -------------------------
        # TECLADO
        # -------------------------
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_F2:
                self.rename_current()

            if event.key == pygame.K_DELETE:
                self.delete_current()

    # ------------------------------------------------
    # ACTIONS
    # ------------------------------------------------

    def create_animation(self):

        project = self.state.project

        root = tk.Tk()
        root.withdraw()

        name = simpledialog.askstring("Nova Animação", "Nome:")

        root.destroy()

        if not name:
            return

        if name in project.animations:
            print("Já existe")
            return

        project.add_animation(name)

        if not hasattr(project, "animation_order"):
            project.animation_order = []

        project.animation_order.append(name)

        self.state.set_animation(name)

    def rename_current(self):

        project = self.state.project
        current = self.state.current_animation

        if not current:
            return

        root = tk.Tk()
        root.withdraw()

        new_name = simpledialog.askstring("Renomear", "Novo nome:", initialvalue=current)

        root.destroy()

        if not new_name or new_name == current:
            return

        if new_name in project.animations:
            print("Nome já existe")
            return

        # rename dict
        project.animations[new_name] = project.animations.pop(current)

        # rename ordem
        idx = project.animation_order.index(current)
        project.animation_order[idx] = new_name

        self.state.set_animation(new_name)

    def delete_current(self):

        project = self.state.project
        current = self.state.current_animation

        if not current:
            return

        if len(project.animation_order) <= 1:
            print("Não pode deletar a última")
            return

        root = tk.Tk()
        root.withdraw()

        confirm = messagebox.askyesno("Remover", f"Deletar '{current}'?")

        root.destroy()

        if not confirm:
            return

        del project.animations[current]
        project.animation_order.remove(current)

        self.state.set_animation(project.animation_order[0])

    # ------------------------------------------------
    # DRAW
    # ------------------------------------------------

    def draw(self, screen):

        rect = self.editor.layout.animation_list
        project = self.state.project

        pygame.draw.rect(screen, (35, 35, 35), rect)

        title = self.font.render("ANIMATIONS", True, (180, 180, 180))
        screen.blit(title, (rect.x + 6, rect.y + 4))

        pygame.draw.line(screen, (60, 60, 60),
                         (rect.x, rect.y + 24),
                         (rect.right, rect.y + 24))

        self.items.clear()
        self.rects.clear()

        if not project:
            return

        order = project.animation_order

        y = rect.y + 30 - self.scroll
        mx, my = pygame.mouse.get_pos()

        for i, name in enumerate(order):

            r = pygame.Rect(rect.x + 6, y, rect.width - 12, 22)

            if r.bottom < rect.y or r.top > rect.bottom:
                y += 26
                continue

            if name == self.state.current_animation:
                color = (60, 110, 200)
            elif r.collidepoint(mx, my):
                color = (80, 80, 80)
            else:
                color = (55, 55, 55)

            pygame.draw.rect(screen, color, r)

            # destaque drag
            if i == self.drag_index:
                pygame.draw.rect(screen, (200, 200, 200), r, 2)

            txt = self.font.render(name, True, (230, 230, 230))
            screen.blit(txt, (r.x + 6, r.y + 3))

            self.items.append(name)
            self.rects.append(r)

            y += 26

        # botão add
        self.add_rect = pygame.Rect(rect.x + 6, rect.bottom - 28, rect.width - 12, 22)

        pygame.draw.rect(screen, (90, 90, 90), self.add_rect)

        txt = self.font.render("+ Add", True, (255, 255, 255))
        screen.blit(txt, (
            self.add_rect.centerx - txt.get_width() // 2,
            self.add_rect.centery - txt.get_height() // 2
        ))

        content_height = len(order) * 26
        visible_height = rect.height - 50

        self.max_scroll = max(0, content_height - visible_height)

        # CONTEXT MENU
        if self.context_menu:

            x, y, index = self.context_menu

            pygame.draw.rect(screen, (40, 40, 40), (x, y, 120, 50))
            pygame.draw.rect(screen, (120, 120, 120), (x, y, 120, 50), 1)

            for i, opt in enumerate(["Rename", "Delete"]):

                r = pygame.Rect(x, y + i * 25, 120, 25)

                if r.collidepoint(mx, my):
                    pygame.draw.rect(screen, (70, 70, 70), r)

                txt = self.font.render(opt, True, (220, 220, 220))
                screen.blit(txt, (r.x + 6, r.y + 4))
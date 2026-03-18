import pygame
from game.session import session


class SpriteList:

    def __init__(self, editor):

        self.editor = editor
        self.items = []

        # cache de fonte (performance)
        self.font = pygame.font.SysFont("arial", 16)

    # ------------------------------------------------
    # DRAW
    # ------------------------------------------------

    def draw(self, screen):

        rect = self.editor.layout.sprite_list

        y = rect.y + 10
        self.items.clear()

        mx, my = pygame.mouse.get_pos()

        for sprite in session.sprite_list:

            r = pygame.Rect(rect.x + 10, y, rect.width - 20, 24)

            # -------------------------
            # CORES (hover / selecionado)
            # -------------------------

            if sprite["id"] == self.editor.selected_sprite_id:
                color = (40, 100, 180)  # azul selecionado

            elif r.collidepoint(mx, my):
                color = (90, 90, 90)  # hover

            else:
                color = (70, 70, 70)

            pygame.draw.rect(screen, color, r)

            # texto
            txt = self.font.render(sprite["name"], True, (220, 220, 220))
            screen.blit(txt, (r.x + 6, r.y + 4))

            self.items.append((r, sprite["id"]))

            y += 30

    # ------------------------------------------------
    # INPUT
    # ------------------------------------------------

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = pygame.mouse.get_pos()

            for rect, sprite_id in self.items:

                if rect.collidepoint(mx, my):

                    # -------------------------
                    # SELEÇÃO VISUAL
                    # -------------------------

                    self.editor.selected_sprite_id = sprite_id

                    # -------------------------
                    # RESET ESTADO
                    # -------------------------

                    self.editor.state.reset_selection()
                    self.editor.canvas.reset()

                    # reset preview
                    self.editor.preview.player.frame_index = 0

                    # -------------------------
                    # REQUEST SERVER
                    # -------------------------

                    from network.sender import request_sprite_project

                    request_sprite_project(
                        self.editor.client_socket,
                        sprite_id
                    )

                    return
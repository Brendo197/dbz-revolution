import pygame
from game.session import session
from launcher.ui.top_bar import TopBar
from launcher.ui.bottom_menu import BottomMenu
from launcher.ui.mission_panel import MissionPanel
from launcher.ui.chat_panel import ChatPanel
from launcher.ui.panel_manager import PanelManager
from launcher.ui.config_panel import ConfigPanel
from network.sender import send_open_admin_packet
from network.sender import send_chat
from game.session import session


def game_screen(screen, client_socket):
    clock = pygame.time.Clock()
    session.client_socket = client_socket
    # ===== UI ELEMENTS =====
    top_bar = TopBar(screen.get_width(), screen.get_height())
    bottom_menu = BottomMenu(screen.get_width(), screen.get_height())
    mission_panel = MissionPanel(screen.get_width(), screen.get_height())
    chat_panel = ChatPanel(
        screen.get_width(),
        screen.get_height(),
        bottom_menu.height
    )
    panel_manager = PanelManager(screen.get_width(), screen.get_height())
    config_panel = ConfigPanel(screen.get_width(), screen.get_height())

    running = True

    while running:
        dt = clock.tick(60) / 1000

        # ================= EVENTS =================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            # 🔥 DETECTA INSERT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_INSERT:
                    send_open_admin_packet(client_socket)  # só envia pedido

            # ================= CHAT INPUT =================
            msg = chat_panel.handle_event(event)
            if msg:
                send_chat(client_socket, msg)

            # ================= CONFIG PANEL =================
            if panel_manager.active_panel == "config":
                result = config_panel.handle_event(event)

                if result:
                    resolution_index, new_res = result
                    return ("reload_game", resolution_index, new_res)

            # ================= BOTTOM MENU =================
            selected = bottom_menu.handle_event(event)

            if selected:
                if selected == "arena":
                    return "battle"
                else:
                    panel_manager.open(selected)

        # ================= UPDATE =================
        panel_manager.update(dt)

        # ================= DRAW =================
        screen.fill((15, 18, 25))

        mission_panel.draw(screen)
        chat_panel.draw(screen,dt)

        top_bar.draw(screen)
        bottom_menu.draw(screen)

        panel_manager.draw(screen)

        # 🔥 ADMIN PANEL
        if session.open_admin_flag:
            from launcher.ui.admin_panel import open_admin_window
            open_admin_window()
            session.open_admin_flag = False

        if panel_manager.active_panel == "config":
            config_panel.draw(screen)

        pygame.display.flip()
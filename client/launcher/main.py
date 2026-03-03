import os
os.environ["SDL_VIDEO_CENTERED"] = "1"

import pygame

from core.config import resource_path
from core.config_manager import load_config, save_config

from launcher.screens.loading import loading_screen
from launcher.screens.login import login_screen
from launcher.screens.register import register_screen
from launcher.screens.create_character import create_character_screen
from launcher.screens.game import game_screen

from network.socket_client import ClientSocket


# ==========================================
# RESOLUÇÕES DISPONÍVEIS
# ==========================================
def get_resolution(index: int):
    resolutions = {
        1: (800, 608),
        2: (1280, 704),
        3: (1344, 704),
        4: (1600, 832),
        5: (1856, 960),
        6: (2432, 960),
    }
    return resolutions.get(index, (1280, 704))


# ==========================================
# MAIN
# ==========================================
def main():
    pygame.init()

    # ===== CARREGA CONFIG =====
    config = load_config()
    resolution_index = config.get("resolution", 2)

    # ===== CARREGA ÍCONE UMA VEZ =====
    icon_surface = pygame.image.load(
        resource_path("assets/ui/icon.ico")
    )

    # ======================================
    # FUNÇÃO PARA RECRIAR JANELA CENTRALIZADA
    # ======================================
    def recreate_window(size):
        pygame.display.quit()
        pygame.display.init()

        screen = pygame.display.set_mode(size)

        pygame.display.set_caption("DBZ Revolution")
        pygame.display.set_icon(icon_surface)

        return screen

    # ===== LOGIN COMEÇA PEQUENO =====
    screen = recreate_window((678, 570))

    # ===== LOADING =====
    if not loading_screen(screen):
        pygame.quit()
        return

    # ===== CONECTA AO SERVIDOR =====
    try:
        client_socket = ClientSocket("127.0.0.1", 4000)
    except Exception as e:
        print("[CLIENT] Erro ao conectar:", e)
        pygame.quit()
        return

    current_screen = "login"

    # ======================================
    # LOOP PRINCIPAL
    # ======================================
    while current_screen:

        # ================= LOGIN =================
        if current_screen == "login":
            result = login_screen(screen, client_socket)

            # Se entrou no game → aplica resolução salva
            if result == "game":
                width, height = get_resolution(resolution_index)
                screen = recreate_window((width, height))

            current_screen = result

        # ================= REGISTER =================
        elif current_screen == "register":
            current_screen = register_screen(screen, client_socket)

        # ================= CREATE CHARACTER =================
        elif current_screen == "create_character":
            current_screen = create_character_screen(screen, client_socket)

        # ================= GAME =================
        elif current_screen == "game":
            result = game_screen(screen, client_socket)

            # 🔥 Mudou resolução dentro do jogo
            if isinstance(result, tuple) and result[0] == "reload_game":
                _, new_index, new_res = result

                # Salva no config.json
                config["resolution"] = new_index
                save_config(config)

                resolution_index = new_index

                # Recria janela centralizada
                screen = recreate_window(new_res)

                current_screen = "game"
            else:
                current_screen = result

    # ===== ENCERRA =====
    client_socket.close()
    pygame.quit()


if __name__ == "__main__":
    main()
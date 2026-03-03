import pygame
from core.config import resource_path
from launcher.ui.input import TextInput
from launcher.ui.button import InvisibleButton
from launcher.ui.toast import Toast
from network.sender import create_character
from game.session import session  # onde você guarda account_id


def create_character_screen(screen, client_socket):
    # ===== CONTROLE DE ESTADO =====
    waiting_response = False
    server_result = None

    def on_create_result(result):
        nonlocal waiting_response, server_result
        server_result = result
        waiting_response = False

    # ===== BACKGROUND =====
    bg = pygame.image.load(
        resource_path("assets/ui/newchar_bg.png")
    ).convert()
    bg = pygame.transform.scale(bg, screen.get_size())

    # ===== INPUT =====
    nickname_input = TextInput(
        233, 228, 218, 26,
        font_size=16,
        text_color=(255, 255, 255)
    )

    # ===== BOTÕES =====
    btn_create = InvisibleButton(280, 387, 118, 34)

    btn_home = InvisibleButton(47, 498, 133, 40)
    btn_register = InvisibleButton(199, 498, 133, 40)
    btn_config = InvisibleButton(352, 498, 133, 40)
    btn_exit = InvisibleButton(504, 498, 133, 40)

    # ===== TOAST =====
    toast = Toast(screen.get_width())

    clock = pygame.time.Clock()

    while True:
        # ===== DESENHO =====
        screen.blit(bg, (0, 0))
        nickname_input.draw(screen)
        toast.draw(screen)
        pygame.display.flip()

        # ===== RESPOSTA DO SERVIDOR =====
        if server_result:
            if server_result.get("success"):
                toast.show(
                    "Personagem criado com sucesso!",
                    color=(80, 255, 80),
                    duration=1.2
                )
                return "game"
            else:
                toast.show(
                    server_result.get("error", "Erro ao criar personagem"),
                    color=(255, 80, 80)
                )

            server_result = None

        # ===== EVENTOS =====
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            nickname_input.handle_event(event)

            # ===== CRIAR PERSONAGEM =====
            if btn_create.clicked(event) and not waiting_response:
                nickname = nickname_input.text.strip()

                if len(nickname) < 4:
                    toast.show(
                        "Nickname deve ter ao menos 4 caracteres",
                        color=(255, 80, 80)
                    )
                    continue

                waiting_response = True
                toast.show("Criando personagem...", color=(255, 255, 255))

                create_character(
                    client_socket,
                    nickname,
                    "1",  # warrior inicial padrão
                    on_create_result
                )

            # ===== NAVEGAÇÃO =====
            if btn_home.clicked(event):
                return "login"

            if btn_register.clicked(event):
                return "register"

            if btn_config.clicked(event):
                toast.show("Configurações em breve", color=(200, 200, 200))

            if btn_exit.clicked(event):
                return None

        clock.tick(60)

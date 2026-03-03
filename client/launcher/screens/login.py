import pygame

from core.config import resource_path
from core.config_manager import load_config, save_config

from launcher.ui.input import TextInput
from launcher.ui.button import InvisibleButton
from launcher.ui.checkbox import Checkbox
from launcher.ui.toast import Toast

from protocol.buffer import Buffer
from protocol.opcodes import C_LOGIN
from network.sender import send_packet

from game.session import session


def login_screen(screen, client_socket):
    # ===== CONTROLE DE ESTADO =====
    waiting_response = False

    # ===== BACKGROUND =====
    bg = pygame.image.load(
        resource_path("assets/ui/login_bg.png")
    ).convert()
    bg = pygame.transform.scale(bg, screen.get_size())

    # ===== INPUTS =====
    login_input = TextInput(
        234, 278, 218, 26,
        font_size=16,
        text_color=(255, 255, 255)
    )

    pass_input = TextInput(
        234, 338, 218, 26,
        password=True,
        font_size=16,
        text_color=(255, 255, 255)
    )

    # ===== CHECKBOXES =====
    chk_save = Checkbox(237, 368, 12)
    chk_auto = Checkbox(344, 368, 12)

    # ===== CARREGAR CONFIG =====
    config = load_config()
    if config.get("save_password"):
        login_input.text = config.get("username", "")
        pass_input.text = config.get("password", "")
        chk_save.checked = True

    chk_font = pygame.font.SysFont("georgia", 10)

    # ===== BOTÕES =====
    btn_login = InvisibleButton(280, 387, 118, 34)

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

        login_input.draw(screen)
        pass_input.draw(screen)

        chk_save.draw(screen)
        chk_auto.draw(screen)

        screen.blit(
            chk_font.render("Salvar Senha?", True, (255, 255, 255)),
            (237 + 16, 368 - 1)
        )
        screen.blit(
            chk_font.render("Auto Relogar?", True, (255, 255, 255)),
            (344 + 16, 368 - 1)
        )

        toast.draw(screen)
        pygame.display.flip()

        # ===== RESPOSTA DO SERVIDOR (VIA SESSION) =====
        if session.logged_in:
            if chk_save.checked:
                save_config({
                    "save_password": True,
                    "username": login_input.text,
                    "password": pass_input.text
                })
            else:
                save_config({"save_password": False})

            return "game" if session.has_character else "create_character"

        if session.login_error:
            toast.show(session.login_error, color=(255, 80, 80))
            session.login_error = None
            waiting_response = False

        # ===== EVENTOS =====
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            login_input.handle_event(event)
            pass_input.handle_event(event)

            chk_save.handle_event(event)
            chk_auto.handle_event(event)

            # ===== LOGIN =====
            if btn_login.clicked(event) and not waiting_response:
                if len(login_input.text) < 4 or len(pass_input.text) < 4:
                    toast.show(
                        "Login e senha devem ter ao menos 4 caracteres",
                        color=(255, 80, 80)
                    )
                    continue

                waiting_response = True
                toast.show("Entrando...", color=(255, 255, 255))

                # 🔥 SALVA NA SESSION (FALTAVA ISSO)
                session.username = login_input.text
                session.password = pass_input.text

                buffer = Buffer()
                buffer.write_byte(C_LOGIN)
                buffer.write_string(login_input.text)
                buffer.write_string(pass_input.text)

                send_packet(client_socket, buffer)

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

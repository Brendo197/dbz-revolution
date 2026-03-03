import pygame

from core.config import resource_path

from launcher.ui.input import TextInput
from launcher.ui.button import InvisibleButton
from launcher.ui.toast import Toast

from network.sender import send_register_step1
from network import receiver
from game.session import session

def register_screen(screen, client_socket):
    waiting_response = False
    register_result = None

    toast = Toast(screen.get_width())

    # ===== CALLBACK STEP 1 (REDE) =====
    def on_register_step1_result(success):
        nonlocal register_result
        print("[UI] CALLBACK REGISTER STEP1 CHAMADO ->", success)
        register_result = success

    print("[UI] REGISTER SCREEN INICIADA")

    # ===== BACKGROUND =====
    bg = pygame.image.load(
        resource_path("assets/ui/register_bg.png")
    ).convert()
    bg = pygame.transform.scale(bg, screen.get_size())

    # ===== INPUTS =====
    input_login = TextInput(233, 228, 218, 26, font_size=16, text_color=(255, 255, 255))
    input_pass = TextInput(233, 284, 218, 26, password=True, font_size=16, text_color=(255, 255, 255))
    input_pass2 = TextInput(233, 339, 218, 26, password=True, font_size=16, text_color=(255, 255, 255))

    # ===== BOTÕES =====
    btn_create = InvisibleButton(280, 387, 118, 34)

    btn_home = InvisibleButton(47, 498, 133, 40)
    btn_register = InvisibleButton(199, 498, 133, 40)
    btn_config = InvisibleButton(352, 498, 133, 40)
    btn_exit = InvisibleButton(504, 498, 133, 40)

    clock = pygame.time.Clock()

    # ================= LOOP =================
    while True:

        # ===== DEBUG DO RESULTADO =====
        if register_result is not None:
            print("[UI] REGISTER_RESULT RECEBIDO ->", register_result)
            waiting_response = False

            if register_result:
                print("[UI] REGISTER OK -> TROCANDO PARA LOGIN")
                return "create_character"
            else:
                print("[UI] REGISTER FAIL -> MOSTRANDO ERRO")
                toast.show("Erro ao validar dados", color=(255, 80, 80))

            register_result = None

        screen.blit(bg, (0, 0))

        input_login.draw(screen)
        input_pass.draw(screen)
        input_pass2.draw(screen)

        toast.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[UI] QUIT")
                return None

            input_login.handle_event(event)
            input_pass.handle_event(event)
            input_pass2.handle_event(event)

            # ===== CRIAR CONTA (STEP 1) =====
            if btn_create.clicked(event) and not waiting_response:

                print("[UI] BOTÃO CRIAR CLICADO")

                if not client_socket:
                    print("[UI] CLIENT SOCKET INVALIDO")
                    toast.show("Servidor offline", color=(255, 80, 80))
                    continue

                if len(input_login.text) < 4 or len(input_pass.text) < 4:
                    print("[UI] LOGIN/SENHA CURTOS")
                    toast.show("Login e senha muito curtos", color=(255, 80, 80))
                    continue

                if input_pass.text != input_pass2.text:
                    print("[UI] SENHAS NÃO CONFEREM")
                    toast.show("As senhas não conferem", color=(255, 80, 80))
                    continue

                waiting_response = True
                print("[UI] ENVIANDO REGISTER STEP1")
                toast.show("Validando dados...", color=(255, 255, 255))

                receiver.register_step1_callback = on_register_step1_result

                session.username = input_login.text
                session.password = input_pass.text

                try:
                    send_register_step1(
                        client_socket,
                        input_login.text,
                        input_pass.text,
                        input_pass2.text
                    )
                    print("[UI] REGISTER STEP1 ENVIADO")
                except Exception as e:
                    waiting_response = False
                    print("[UI] ERRO AO ENVIAR REGISTER:", e)
                    toast.show(f"Erro ao enviar: {e}", (255, 80, 80))

            # ===== NAVEGAÇÃO =====
            if btn_home.clicked(event):
                print("[UI] HOME")
                return "login"

            if btn_register.clicked(event):
                print("[UI] JÁ NA TELA REGISTER")
                toast.show("Você já está nessa tela", (180, 180, 180))

            if btn_config.clicked(event):
                print("[UI] CONFIG")
                toast.show("Configurações em breve", color=(200, 200, 200))

            if btn_exit.clicked(event):
                print("[UI] EXIT")
                return None

        clock.tick(60)

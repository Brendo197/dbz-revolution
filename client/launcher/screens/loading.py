import pygame
import time

from core.config import resource_path
from protocol.buffer import Buffer
from protocol.opcodes import C_PING
from game.session import session


def loading_screen(screen, client_socket=None):
    bg = pygame.image.load(
        resource_path("assets/ui/loading.png")
    ).convert()
    bg = pygame.transform.scale(bg, screen.get_size())

    font = pygame.font.SysFont("arial", 20)

    steps = [
        "Iniciando...",
        "Verificando versão...",
        "Carregando configurações...",
        "Preparando ambiente..."
    ]

    current_step = 0
    last_change = time.time()
    last_ping = 0

    clock = pygame.time.Clock()

    while True:
        now = time.time()

        # ===== PING NO SERVIDOR =====
        if client_socket and now - last_ping > 1:
            last_ping = now
            buffer = Buffer()
            buffer.write_byte(C_PING)
            client_socket.send(buffer.get_bytes())

        # ===== DESENHO =====
        screen.blit(bg, (0, 0))

        screen.blit(
            font.render(steps[current_step], True, (255, 255, 255)),
            (20, screen.get_height() - 60)
        )

        # ===== STATUS DO SERVIDOR (SEMPRE VIA SESSION) =====
        if session.server_online:
            server_text = "Servidor: Online"
            color = (80, 255, 80)
        else:
            server_text = "Servidor: Offline"
            color = (255, 80, 80)

        screen.blit(
            font.render(server_text, True, color),
            (20, screen.get_height() - 35)
        )

        pygame.display.flip()

        # ===== EVENTOS =====
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # ===== ETAPAS =====
        if now - last_change > 1:
            last_change = now
            current_step += 1

            if current_step >= len(steps):
                return True

        clock.tick(60)

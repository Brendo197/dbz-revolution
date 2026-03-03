import pygame
from game.scene_manager import SceneManager
from game.scenes.world_scene import WorldScene
from network.sender import send_open_admin_packet

def game_loop(screen):
    clock = pygame.time.Clock()
    manager = SceneManager()

    # Cena inicial do jogo
    manager.change_scene(WorldScene(manager))

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None


            manager.handle_event(event)

        manager.update(dt)
        manager.draw(screen)

        pygame.display.flip()

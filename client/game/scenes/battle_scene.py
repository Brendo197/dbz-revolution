import pygame
from game.scenes.base_scene import BaseScene

class BattleScene(BaseScene):
    def on_enter(self, data=None):
        print("[SCENE] Entrou na BATALHA")
        self.font = pygame.font.SysFont("arial", 20)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from game.scenes.world_scene import WorldScene
                self.manager.change_scene(WorldScene(self.manager))

    def draw(self, screen):
        screen.fill((30, 30, 30))
        text = self.font.render(
            "BATTLE SCENE - ESC para voltar",
            True,
            (255, 80, 80)
        )
        screen.blit(text, (20, 20))

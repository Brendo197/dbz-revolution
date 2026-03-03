import pygame
from game.scenes.base_scene import BaseScene

class WorldScene(BaseScene):
    def on_enter(self, data=None):
        print("[SCENE] Entrou no WORLD")

        self.font = pygame.font.SysFont("arial", 20)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                # DEBUG: entrar em batalha
                from game.scenes.battle_scene import BattleScene
                self.manager.change_scene(BattleScene(self.manager))

    def draw(self, screen):
        screen.fill((0, 0, 0))
        text = self.font.render(
            "WORLD SCENE - Aperte B para batalha",
            True,
            (255, 255, 255)
        )
        screen.blit(text, (20, 20))

from game.scenes.base_scene import BaseScene

class EmptyScene(BaseScene):
    def draw(self, screen):
        screen.fill((0, 0, 0))

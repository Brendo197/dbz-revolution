class SceneManager:
    def __init__(self):
        self.current_scene = None

    def change_scene(self, new_scene, data=None):
        if self.current_scene:
            self.current_scene.on_exit()

        self.current_scene = new_scene
        self.current_scene.on_enter(data)

    def handle_event(self, event):
        if self.current_scene:
            self.current_scene.handle_event(event)

    def update(self, dt):
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)

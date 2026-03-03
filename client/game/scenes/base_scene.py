class BaseScene:
    def __init__(self, manager):
        self.manager = manager

    def on_enter(self, data=None):
        """Chamado quando a cena entra"""
        pass

    def on_exit(self):
        """Chamado quando a cena sai"""
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

from .animation import Animation

class SpriteProject:

    def __init__(self, sprite_id=0):

        self.id = sprite_id

        self.animations = {}
        self.animation_order = []
        self.name = ""
        self.sheet = None



    def add_animation(self, name):

        if name not in self.animations:

            self.animations[name] = Animation(name)


    def get_animation(self, name):

        return self.animations.get(name)
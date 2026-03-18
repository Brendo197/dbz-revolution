class Animation:

    def __init__(self, name):

        self.name = name

        self.frames = []

        # tempo padrão
        self.tick = 120

        # animação loop
        self.loop = True


    # -------------------------
    # SERIALIZE
    # -------------------------

    def to_dict(self):

        return {
            "name": self.name,
            "tick": self.tick,
            "loop": self.loop,
            "frames": [frame.to_dict() for frame in self.frames]
        }


    # -------------------------
    # DESERIALIZE
    # -------------------------

    @staticmethod
    def from_dict(data):

        anim = Animation(data["name"])

        anim.tick = data.get("tick", 120)
        anim.loop = data.get("loop", True)

        from .frame import Frame

        anim.frames = [
            Frame.from_dict(f)
            for f in data.get("frames", [])
        ]

        return anim

    def add_frame(self, x, y, w, h):
        frame = Frame(x, y, w, h)
        self.frames.append(frame)
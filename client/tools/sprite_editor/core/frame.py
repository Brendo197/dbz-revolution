class Frame:

    def __init__(self, x, y, w, h):

        # posição na sprite sheet
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # alinhamento do personagem
        self.origin_x = 0
        self.origin_y = 0

        # deslocamento visual
        self.offset_x = 0
        self.offset_y = 0

        # override de tempo
        self.tick_override = None

        # frame de ataque
        self.attack_frame = False

        # colisões
        self.hitboxes = []
        self.hurtboxes = []

    # -------------------------
    # SERIALIZE
    # -------------------------

    def to_dict(self):

        return {
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h,

            "origin_x": self.origin_x,
            "origin_y": self.origin_y,

            "offset_x": self.offset_x,
            "offset_y": self.offset_y,

            "tick_override": self.tick_override,
            "attack_frame": self.attack_frame,

            "hitboxes": self.hitboxes,
            "hurtboxes": self.hurtboxes
        }

    # -------------------------
    # DESERIALIZE
    # -------------------------

    @staticmethod
    def from_dict(data):

        frame = Frame(
            data["x"],
            data["y"],
            data["w"],
            data["h"]
        )

        frame.origin_x = data.get("origin_x", 0)
        frame.origin_y = data.get("origin_y", 0)

        frame.offset_x = data.get("offset_x", 0)
        frame.offset_y = data.get("offset_y", 0)

        frame.tick_override = data.get("tick_override")
        frame.attack_frame = data.get("attack_frame", False)

        frame.hitboxes = data.get("hitboxes", [])
        frame.hurtboxes = data.get("hurtboxes", [])

        return frame
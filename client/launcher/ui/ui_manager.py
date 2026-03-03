class UIManager:
    BASE_WIDTH = 1280
    BASE_HEIGHT = 704

    def __init__(self, screen_width, screen_height):
        self.scale_x = screen_width / self.BASE_WIDTH
        self.scale_y = screen_height / self.BASE_HEIGHT

    def scale_rect(self, x, y, w, h):
        return (
            int(x * self.scale_x),
            int(y * self.scale_y),
            int(w * self.scale_x),
            int(h * self.scale_y)
        )

    def scale_value_x(self, value):
        return int(value * self.scale_x)

    def scale_value_y(self, value):
        return int(value * self.scale_y)
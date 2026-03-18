class AnimationPlayer:

    def __init__(self):

        self.animation = None
        self.frame_index = 0
        self.timer = 0

        self.playing = True


    # -------------------------
    # PLAY
    # -------------------------

    def play(self, animation):

        if self.animation != animation:

            self.animation = animation
            self.frame_index = 0
            self.timer = 0


    # -------------------------
    # STOP
    # -------------------------

    def stop(self):

        self.playing = False


    # -------------------------
    # RESUME
    # -------------------------

    def resume(self):

        self.playing = True


    # -------------------------
    # SET FRAME
    # -------------------------

    def set_frame(self, index):

        if not self.animation:
            return

        if not self.animation.frames:
            return

        self.frame_index = max(0, min(index, len(self.animation.frames) - 1))


    # -------------------------
    # UPDATE
    # -------------------------

    def update(self, dt):

        if not self.playing:
            return

        if not self.animation:
            return

        if not self.animation.frames:
            return

        frame = self.animation.frames[self.frame_index]

        tick = frame.tick_override if frame.tick_override is not None else self.animation.tick

        if tick <= 0:
            tick = 1

        self.timer += dt

        # while evita travamentos quando dt > tick
        while self.timer >= tick:

            self.timer -= tick
            self.frame_index += 1

            if self.frame_index >= len(self.animation.frames):

                if self.animation.loop:
                    self.frame_index = 0
                else:
                    self.frame_index = len(self.animation.frames) - 1
                    break


    # -------------------------
    # GET FRAME
    # -------------------------

    def get_frame(self):

        if not self.animation:
            return None

        if not self.animation.frames:
            return None

        return self.animation.frames[self.frame_index]
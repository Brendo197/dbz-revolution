class EditorState:

    def __init__(self):

        self.project = None

        # animação atual
        self.current_animation = None

        self.current_frame_index = None

        self.selection_rect = None

        self.current_tool = "select"
        self.snap_to_grid = False
        self.listeners = []
        self.selections = []
        self.preview_selection = None
        self.slice_previews = []
        self.hover_selection = None
        self.animation_frames = []
        # preview
        self.preview_timer = 0
        self.preview_index = 0
    # -------------------------
    # LISTENERS
    # -------------------------

    def add_listener(self, func):

        self.listeners.append(func)

    def notify(self):

        for func in self.listeners:
            func()

    def get_current_sprite(self):

        if not self.project:
            return None

        return self.project
    # -------------------------
    # PROJECT
    # -------------------------

    def set_project(self, project):

        self.project = project

        self.current_animation = None
        self.current_frame_index = None
        self.selection_rect = None

        self.notify()

    # -------------------------
    # ANIMATION
    # -------------------------

    def set_animation(self, name):

        if not self.project:
            return

        self.current_animation = name
        self.current_frame_index = None

        self.notify()

    # -------------------------
    # FRAME
    # -------------------------

    def set_frame(self, index):

        self.current_frame_index = index

        self.notify()

    # -------------------------
    # TOOL
    # -------------------------

    def set_tool(self, tool):

        self.current_tool = tool

        self.notify()

    # -------------------------
    # GET CURRENT ANIMATION
    # -------------------------

    def get_current_animation(self):

        if not self.project or not self.current_animation:
            return None

        return self.project.animations.get(self.current_animation)

    # -------------------------
    # GET CURRENT FRAME
    # -------------------------

    def get_current_frame(self):

        anim = self.get_current_animation()

        if not anim:
            return None

        if self.current_frame_index is None:
            return None

        if self.current_frame_index >= len(anim.frames):
            return None

        return anim.frames[self.current_frame_index]

    def reset_selection(self):

        self.selection_rect = None

        if hasattr(self, "selections"):
            self.selections.clear()

        if hasattr(self, "slice_previews"):
            self.slice_previews.clear()

        self.current_frame_index = 0
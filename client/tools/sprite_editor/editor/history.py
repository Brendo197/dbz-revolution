class History:

    def __init__(self, limit=100):

        # pilhas
        self.undo_stack = []
        self.redo_stack = []

        # limite de histórico
        self.limit = limit

    # -------------------------
    # PUSH ACTION
    # -------------------------

    def push(self, undo_action, redo_action):

        """
        undo_action -> função para desfazer
        redo_action -> função para refazer
        """

        self.undo_stack.append((undo_action, redo_action))

        # limpar redo quando nova ação acontece
        self.redo_stack.clear()

        # limitar histórico
        if len(self.undo_stack) > self.limit:
            self.undo_stack.pop(0)

    # -------------------------
    # UNDO
    # -------------------------

    def undo(self):

        if not self.undo_stack:
            return

        undo_action, redo_action = self.undo_stack.pop()

        # executar undo
        undo_action()

        # guardar para redo
        self.redo_stack.append((undo_action, redo_action))

    # -------------------------
    # REDO
    # -------------------------

    def redo(self):

        if not self.redo_stack:
            return

        undo_action, redo_action = self.redo_stack.pop()

        # executar redo
        redo_action()

        # voltar para undo
        self.undo_stack.append((undo_action, redo_action))

    # -------------------------
    # CLEAR
    # -------------------------

    def clear(self):

        self.undo_stack.clear()
        self.redo_stack.clear()
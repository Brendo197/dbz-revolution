import time
import threading


class GameSession:
    def __init__(self):
        self.reset()

        self._running = False
        self._ping_thread = None

        self.chat_unread = {
            "global": 0,
            "system": 0,
            "guild": 0
        }

        self.active_chat_channel = "global"

        self.warrior_templates = []


        self.open_admin_flag = False
        self.client_socket = None
        self.editor_token = None
    def reset(self):

        # ===== SERVER =====
        self.server_online = False
        self.last_pong = 0

        # ===== AUTH =====
        self.logged_in = False
        self.account_id = None

        self.username = None
        self.password = None

        self.nickname = None
        self.has_character = False
        self.is_admin = False

        # ===== FLAGS =====
        self.login_error = None
        self.register_success = False
        self.register_error = None

        # ===== CHAT =====
        self.chat_messages = {
            "global": [],
            "system": [],
            "guild": []
        }

        self.chat_unread = {
            "global": 0,
            "system": 0,
            "guild": 0
        }

        # ===== SPRITES =====
        self.sprite_list = []
        self.sprite_project = None
        self.sprite_cache = {}
        self.current_sprite_id = None
        self.sprite_project_updated = False
    @property
    def logged(self):
        return self.logged_in

    @property
    def socket(self):
        return self.client_socket
    # =========================
    # LOGIN / REGISTER
    # =========================

    def login_success(self, account_id, nickname, has_character, is_admin=False):
        self.logged_in = True
        self.account_id = account_id
        self.nickname = nickname
        self.has_character = has_character
        self.is_admin = is_admin

        self.login_error = None

    def login_fail(self, message="Login inválido"):
        self.logged_in = False
        self.login_error = message

    def register_ok(self):
        self.register_success = True
        self.register_error = None

    def register_fail(self, message):
        self.register_success = False
        self.register_error = message

    # =========================
    # SERVER STATUS
    # =========================

    def set_server_online(self):
        self.server_online = True

    def set_server_offline(self):
        self.server_online = False

    # =========================
    # PING LOOP
    # =========================

    def start_ping_loop(self, send_ping_func, interval=5):
        if self._running:
            return

        self._running = True

        def loop():
            while self._running:
                send_ping_func()
                time.sleep(interval)

        self._ping_thread = threading.Thread(
            target=loop,
            daemon=True
        )
        self._ping_thread.start()

    def stop(self, clear_session=True):
        self._running = False

        if clear_session:
            self.reset()
            self.server_online = False


# 🔥 instância global
session = GameSession()

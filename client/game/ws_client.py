import websocket
import json
import threading
import time


class WSClient:
    def __init__(self, token):
        self.token = token
        self.ws = None
        self.running = False

    def connect(self):
        self.ws = websocket.WebSocketApp(
            f"ws://127.0.0.1:2004/ws?token={self.token}",
            on_message=self.on_message,
            on_close=self.on_close
        )

        self.running = True

        threading.Thread(
            target=self.ws.run_forever,
            daemon=True
        ).start()

        threading.Thread(
            target=self._ping_loop,
            daemon=True
        ).start()

    def _ping_loop(self):
        while self.running:
            try:
                self.ws.send(json.dumps({"type": "ping"}))
            except:
                break
            time.sleep(5)

    def on_message(self, ws, msg):
        data = json.loads(msg)
        # tratar eventos do jogo

    def on_close(self, ws, code, msg):
        self.running = False

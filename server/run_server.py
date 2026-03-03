from alembic import command
from alembic.config import Config
from core.server import GameServer
from threading import Thread
from gui.server_panel import start_gui

print("[1/2] Aplicando migrations...")
cfg = Config("alembic.ini")
command.upgrade(cfg, "head")
print("[MIGRATIONS] Banco atualizado ✔️")

if __name__ == "__main__":

    server = GameServer(port=4000)

    Thread(target=server.run, daemon=True).start()

    start_gui(server)
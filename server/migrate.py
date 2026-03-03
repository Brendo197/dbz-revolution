from alembic import command
from alembic.config import Config

print("[MIGRATIONS] Aplicando migrations...")

cfg = Config("alembic.ini")
command.upgrade(cfg, "head")

print("[MIGRATIONS] Banco atualizado ✔️")

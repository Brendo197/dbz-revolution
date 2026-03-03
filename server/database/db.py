import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models.base import Base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "dbrdata.db")

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=False,
    future=True
)

SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()


# 🔥 FUNÇÃO PARA CRIAR AS TABELAS
def init_db():
    # Importa todos os models para registrar no Base
    from database.models import (
        account,
        player,
        warrior,
        warrior_template,
        inventory,
        team,
        vip
    )

    Base.metadata.create_all(bind=engine)
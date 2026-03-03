from sqlalchemy import Column, Integer, String, ForeignKey
from database.models.base import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))

    nickname = Column(String(32), unique=True, nullable=False)  # 🔥 ESSENCIAL

    level = Column(Integer)
    exp = Column(Integer)
    battles_wins = Column(Integer)
    battles_loses = Column(Integer)
    bank_zeny = Column(Integer)
    sprite_overworld = Column(Integer)

from sqlalchemy import Column, Integer
from database.models.base import Base


class Vip(Base):
    __tablename__ = "vip"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, nullable=False)
    vip_days = Column(Integer, default=0)

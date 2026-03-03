from sqlalchemy import Column, Integer, String
from database.models.base import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, nullable=False)

    slot = Column(Integer, nullable=False)
    item_id = Column(String, nullable=False)
    item_level = Column(Integer, default=0)

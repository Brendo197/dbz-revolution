from sqlalchemy import Column, Integer
from database.models.base import Base


class Team(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, nullable=False)

    position = Column(Integer, nullable=False)
    warrior_id = Column(Integer, nullable=False)

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.models.base import Base


class PlayerWarrior(Base):
    __tablename__ = "player_warriors"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    template_id = Column(Integer, ForeignKey("warrior_templates.id"))

    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    stars = Column(Integer, default=1)

    bonus_attack = Column(Integer, default=0)
    bonus_defense = Column(Integer, default=0)
    bonus_hp = Column(Integer, default=0)
    bonus_speed = Column(Integer, default=0)

    unused_stat_points = Column(Integer, default=0)
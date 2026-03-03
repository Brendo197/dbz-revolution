# warrior_template.py

from sqlalchemy import Column, Integer, String
from database.models.base import Base


class WarriorTemplate(Base):
    __tablename__ = "warrior_templates"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    # Base stats
    base_hp = Column(Integer, nullable=False)
    base_attack = Column(Integer, nullable=False)
    base_defense = Column(Integer, nullable=False)
    base_speed = Column(Integer, nullable=False)

    # Growth por level
    hp_growth = Column(Integer, nullable=False)
    attack_growth = Column(Integer, nullable=False)
    defense_growth = Column(Integer, nullable=False)
    speed_growth = Column(Integer, nullable=False)

    # Skills
    skill1_id = Column(Integer)
    skill1_unlock_level = Column(Integer, default=1)

    skill2_id = Column(Integer)
    skill2_unlock_level = Column(Integer)

    skill3_id = Column(Integer)
    skill3_unlock_level = Column(Integer)

    # Sprite base
    sprite_base = Column(String)
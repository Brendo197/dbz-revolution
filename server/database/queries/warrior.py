from database.db import get_session
from database.models.player_warrior import PlayerWarrior
from database.models.warrior_template import WarriorTemplate

def create_warrior(player_id: int, warrior_type: str):
    db = get_session()
    try:
        template = db.query(WarriorTemplate).filter(
            WarriorTemplate.id == int(warrior_type)
        ).first()

        if not template:
            raise Exception("Template inválido")

        warrior = PlayerWarrior(
            player_id=player_id,
            template_id=template.id,
            level=1,
            stars=1,
            exp=0
        )

        db.add(warrior)
        db.commit()
        db.refresh(warrior)
        return warrior

    finally:
        db.close()

def get_warriors(player_id: int):
    db = get_session()
    try:
        return db.query(PlayerWarrior).filter(PlayerWarrior.player_id == player_id).all()
    finally:
        db.close()


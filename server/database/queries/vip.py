from database.db import get_session
from database.models.vip import Vip


def create_vip(player_id: int):
    db = get_session()
    try:
        vip = Vip(
            player_id=player_id,
            vip_days=0
        )
        db.add(vip)
        db.commit()
    finally:
        db.close()

def get_vip(player_id: int):
    db = get_session()
    try:
        return db.query(Vip).filter(Vip.player_id == player_id).first()
    finally:
        db.close()

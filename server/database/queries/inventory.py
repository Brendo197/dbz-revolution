from database.db import get_session
from database.models.inventory import Inventory

def create_inventory(player_id: int):
    db = get_session()
    try:
        for slot in range(1, 61):
            inv = Inventory(
                player_id=player_id,
                slot=slot,
                item_id="empty",
                item_level=0
            )
            db.add(inv)
        db.commit()
    finally:
        db.close()

def get_inventory(player_id: int):
    db = get_session()
    try:
        return db.query(Inventory).filter(Inventory.player_id == player_id).order_by(Inventory.slot).all()
    finally:
        db.close()

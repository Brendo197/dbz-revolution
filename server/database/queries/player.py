from database.db import get_session
from database.models.player import Player

def create_player(account_id: int, nickname):
    db = get_session()
    try:
        player = Player(
            account_id=account_id,
            nickname=nickname,  # 🔥 AQUI
            level=1,
            exp=0,
            battles_wins=0,
            battles_loses=0,
            bank_zeny=0,
            sprite_overworld=1
        )
        db.add(player)
        db.commit()
        db.refresh(player)
        return player
    finally:
        db.close()
def get_player_by_account(account_id: int):
    db = get_session()
    try:
        return db.query(Player).filter(Player.account_id == account_id).first()
    finally:
        db.close()

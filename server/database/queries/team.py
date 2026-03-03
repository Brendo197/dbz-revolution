from database.db import get_session
from database.models.team import Team


def create_initial_team(player_id: int, warrior_id: int):
    db = get_session()
    try:
        team = Team(
            player_id=player_id,
            position=1,
            warrior_id=warrior_id
        )
        db.add(team)
        db.commit()
    finally:
        db.close()

def get_team(player_id: int):
    db = get_session()
    try:
        return db.query(Team).filter(Team.player_id == player_id).order_by(Team.position).all()
    finally:
        db.close()

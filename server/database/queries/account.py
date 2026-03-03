from database.db import get_session
from database.models.account import Account

def create_account(login: str, password_hash: str):
    db = get_session()
    try:
        acc = Account(
            login=login,
            password_hash=password_hash
        )
        db.add(acc)
        db.commit()
        db.refresh(acc)
        return acc
    finally:
        db.close()


def get_account_by_login(login: str):
    db = get_session()
    try:
        return db.query(Account).filter(Account.login == login).first()
    finally:
        db.close()

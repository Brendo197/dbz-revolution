import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "dbrdata.db")

def init_schema():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # =========================
    # ACCOUNTS
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        nickname TEXT UNIQUE NOT NULL,
        email TEXT,
        is_admin INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # PLAYER PROFILE
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER NOT NULL,
        
        nickname TEXT UNIQUE NOT NULL,

        level INTEGER DEFAULT 1,
        exp INTEGER DEFAULT 0,

        battles_wins INTEGER DEFAULT 0,
        battles_loses INTEGER DEFAULT 0,

        bank_zeny INTEGER DEFAULT 0,
        sprite_overworld INTEGER DEFAULT 1,

        FOREIGN KEY(account_id) REFERENCES accounts(id)
    )
    """)

    # =========================
    # WARRIORS
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS warriors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER NOT NULL,

        warrior_type TEXT NOT NULL,
        level INTEGER DEFAULT 1,
        exp INTEGER DEFAULT 0,
        evolution INTEGER DEFAULT 0,
        skin INTEGER DEFAULT 0,

        FOREIGN KEY(player_id) REFERENCES players(id)
    )
    """)

    # =========================
    # INVENTORY (1–60)
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER NOT NULL,

        slot INTEGER NOT NULL,
        item_id TEXT NOT NULL,
        item_level INTEGER DEFAULT 1,

        FOREIGN KEY(player_id) REFERENCES players(id)
    )
    """)

    # =========================
    # EQUIPMENT (4 SLOTS)
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        warrior_id INTEGER NOT NULL,

        slot INTEGER NOT NULL,
        item_id TEXT NOT NULL,
        item_level INTEGER DEFAULT 1,

        FOREIGN KEY(warrior_id) REFERENCES warriors(id)
    )
    """)

    # =========================
    # TEAM (5 WARRIORS)
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS team (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER NOT NULL,

        position INTEGER NOT NULL,
        warrior_id INTEGER NOT NULL,

        FOREIGN KEY(player_id) REFERENCES players(id),
        FOREIGN KEY(warrior_id) REFERENCES warriors(id)
    )
    """)

    # =========================
    # VIP
    # =========================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vip (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER NOT NULL,

        vip_days INTEGER DEFAULT 0,

        FOREIGN KEY(player_id) REFERENCES players(id)
    )
    """)

    conn.commit()
    conn.close()

    print("[DB] Schema completo garantido")

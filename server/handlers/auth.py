from protocol.buffer import Buffer
from protocol.opcodes import *
from core.protocol import send_packet
from database.db import get_session
from database.models.player import Player
from database.models.warrior_template import WarriorTemplate

from database.queries import (
    # account
    get_account_by_login,
    create_account,

    # player
    get_player_by_account,
    create_player,

    # game data
    create_inventory,
    create_warrior,
    create_initial_team,
    create_vip,

    get_warriors,
    get_inventory,
    get_team,
    get_vip
)

import hashlib


# =====================================================
# HELPER: BROADCAST SYSTEM MESSAGE
# =====================================================

def broadcast_system_message(server, message):
    out = Buffer()
    out.write_byte(S_CHAT)
    out.write_string("Sistema")
    out.write_string(message)

    for c in server.clients:
        send_packet(c, out)

def handle_register_step1(client, buffer: Buffer):
    try:
        login = buffer.read_string().strip()
        password = buffer.read_string().strip()
        password2 = buffer.read_string().strip()

        print("[SERVER] REGISTER STEP 1 RECEBIDO")

        # Login mínimo
        if len(login) < 4:
            _send_register_fail(
                client,
                REGISTER_FAIL_INVALID,
                "Login deve ter no mínimo 4 caracteres."
            )
            return

        # Senha mínima
        if len(password) < 4:
            _send_register_fail(
                client,
                REGISTER_FAIL_PASSWORD,
                "Senha deve ter no mínimo 4 caracteres."
            )
            return

        # Confirmação
        if password != password2:
            _send_register_fail(
                client,
                REGISTER_FAIL_PASSWORD,
                "As senhas não coincidem."
            )
            return

        # Login já existe
        if get_account_by_login(login):
            _send_register_fail(
                client,
                REGISTER_FAIL_LOGIN_EXISTS,
                "Esse login já está em uso."
            )
            return

        # 🔥 CRIA A CONTA AQUI
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        account = create_account(login, password_hash)

        print("[SERVER] Conta criada:", account.id)

        # Marca no client que está em processo de criação
        client.account_id = account.id

        # Responde OK
        out = Buffer()
        out.write_byte(S_REGISTER_OK_STEP1)
        send_packet(client, out)

    except Exception as e:
        print("[REGISTER STEP1 ERROR]", e)
        _send_register_fail(
            client,
            REGISTER_FAIL_SERVER,
            "Erro interno do servidor."
        )
def handle_register_step2(client, buffer: Buffer):
    try:
        nickname = buffer.read_string().strip()
        warrior_type = buffer.read_string().strip()

        print("[SERVER] REGISTER STEP 2:", nickname, warrior_type)

        # 🔒 Confirma que veio do Step1
        if not hasattr(client, "account_id"):
            _send_register_fail(
                client,
                REGISTER_FAIL_INVALID,
                "Sessão inválida."
            )
            return

        account_id = client.account_id

        # Nick mínimo
        if len(nickname) < 3:
            _send_register_fail(
                client,
                REGISTER_FAIL_INVALID,
                "Nickname deve ter no mínimo 3 caracteres."
            )
            return

        # Nick duplicado
        if nickname_exists(nickname):
            _send_register_fail(
                client,
                REGISTER_FAIL_NICKNAME_EXISTS,
                "Esse nickname já está em uso."
            )
            return

        # 🔥 CRIA PLAYER
        player = create_player(account_id, nickname)

        create_vip(player.id)
        create_inventory(player.id)

        warrior = create_warrior(player.id, warrior_type)
        create_initial_team(player.id, warrior.id)

        print("[SERVER] Personagem criado com sucesso.")

        # Limpa flag temporária
        del client.account_id

        # OK
        out = Buffer()
        out.write_byte(S_REGISTER_OK)
        send_packet(client, out)

    except Exception as e:
        print("[REGISTER STEP2 ERROR]", e)
        _send_register_fail(
            client,
            REGISTER_FAIL_SERVER,
            "Erro interno do servidor."
        )
# =====================================================
# LOGIN
# =====================================================

def handle_login(client, buffer: Buffer):
    login = buffer.read_string()
    password = buffer.read_string()

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    account = get_account_by_login(login)

    if not account:
        _send_login_fail(
            client,
            LOGIN_FAIL_INVALID,
            "Conta não encontrada."
        )
        return

    if account.password_hash != password_hash:
        _send_login_fail(
            client,
            LOGIN_FAIL_INVALID,
            "Senha incorreta."
        )
        return

    # 🔐 Impede múltiplos logins
    for c in client.server.clients:
        if c is not client and getattr(c, "account_id", None) == account.id:
            print(f"[SECURITY] Tentativa de login duplicado da conta {account.login}")
            _send_login_fail(
                client,
                LOGIN_FAIL_MULTIPLE,
                "Essa conta já está logada."
            )
            return

    # só depois que validou:
    client.account = account
    client.is_admin = bool(account.is_admin)

    player = get_player_by_account(account.id)

    # Se não tem personagem ainda
    if not player:
        out = Buffer()
        out.write_byte(S_LOGIN_OK)
        out.write_int(account.id)
        out.write_string("")
        out.write_byte(account.is_admin)
        out.write_byte(0)  # has_character = False

        send_packet(client, out)

        client.account_id = account.id
        client.player_id = None
        return

    # ===== SALVA DADOS NO CLIENT =====
    client.account_id = account.id
    client.player_id = player.id
    client.nickname = player.nickname

    # ===== CARREGA DADOS DO JOGO =====
    warriors = get_warriors(player.id)
    inventory = get_inventory(player.id)
    team = get_team(player.id)
    vip = get_vip(player.id)

    # ===== ENVIA LOGIN OK =====
    out = Buffer()
    out.write_byte(S_LOGIN_OK)

    out.write_int(account.id)
    out.write_string(player.nickname)
    out.write_byte(account.is_admin)
    out.write_byte(1)  # has_character = True

    out.write_int(player.level)
    out.write_int(player.exp)
    out.write_int(player.bank_zeny)
    out.write_int(player.sprite_overworld)
    out.write_int(player.battles_wins)
    out.write_int(player.battles_loses)

    out.write_int(vip.vip_days if vip else 0)

    out.write_int(len(warriors))
    for w in warriors:
        out.write_int(w.id)
        out.write_string(w.warrior_type)
        out.write_int(w.level)
        out.write_int(w.exp)
        out.write_int(w.evolution)
        out.write_int(w.skin)

    out.write_int(len(inventory))
    for item in inventory:
        out.write_int(item.slot)
        out.write_string(item.item_id)
        out.write_int(item.item_level)

    out.write_int(len(team))
    for t in team:
        out.write_int(t.position)
        out.write_int(t.warrior_id)

    send_packet(client, out)

    # ===== MENSAGEM GLOBAL LOGIN =====
    broadcast_system_message(
        client.server,
        f"{player.nickname} logou."
    )

    # ===== MENSAGEM PRIVADA =====
    welcome = Buffer()
    welcome.write_byte(S_CHAT)
    welcome.write_string("Sistema")
    welcome.write_string("Bem-vindo ao DBZ Revolution!")
    send_packet(client, welcome)


# =====================================================
# HELPERS
# =====================================================

def _send_login_fail(client, reason, message):
    out = Buffer()
    out.write_byte(S_LOGIN_FAIL)
    out.write_byte(reason)
    out.write_string(message)
    send_packet(client, out)

def _send_register_fail(client, reason, message):
    out = Buffer()
    out.write_byte(S_REGISTER_FAIL)
    out.write_byte(reason)
    out.write_string(message)
    send_packet(client, out)


def nickname_exists(nickname):
    db = get_session()
    try:
        return db.query(Player).filter(Player.nickname == nickname).first() is not None
    finally:
        db.close()

def handle_open_admin(client):
    if not client.is_admin:
        return  # ignora silenciosamente

    out = Buffer()
    out.write_byte(S_OPEN_ADMIN)
    send_packet(client, out)



def handle_request_warrior_templates(client, buffer):
    print("[ADMIN] Pedido de lista de WarriorTemplates recebido")

    if not getattr(client, "is_admin", False):
        print("[ADMIN] Cliente não é admin.")
        return

    db = get_session()

    try:
        warriors = db.query(WarriorTemplate).all()

        response = Buffer()
        response.write_byte(S_SEND_WARRIOR_TEMPLATES)
        response.write_int(len(warriors))

        for w in warriors:
            response.write_int(w.id)
            response.write_string(w.name)

            response.write_int(w.base_hp or 0)
            response.write_int(w.base_attack or 0)
            response.write_int(w.base_defense or 0)
            response.write_int(w.base_speed or 0)

            response.write_int(w.hp_growth or 0)
            response.write_int(w.attack_growth or 0)
            response.write_int(w.defense_growth or 0)
            response.write_int(w.speed_growth or 0)

            response.write_int(w.skill1_id or 0)
            response.write_int(w.skill1_unlock_level or 0)

            response.write_int(w.skill2_id or 0)
            response.write_int(w.skill2_unlock_level or 0)

            response.write_int(w.skill3_id or 0)
            response.write_int(w.skill3_unlock_level or 0)

            response.write_string(w.sprite_base or "")

        send_packet(client, response)
        print(f"[ADMIN] Enviados {len(warriors)} warrior templates.")

    finally:
        db.close()

def handle_save_warrior_template(client, buffer):

    if not getattr(client, "is_admin", False):
        print("[SECURITY] Tentativa de salvar warrior sem permissão.")
        return

    warrior_id = buffer.read_int()
    name = buffer.read_string().strip()
    sprite = buffer.read_string().strip()

    base_hp = buffer.read_int()
    base_attack = buffer.read_int()
    base_defense = buffer.read_int()
    base_speed = buffer.read_int()

    hp_growth = buffer.read_int()
    attack_growth = buffer.read_int()
    defense_growth = buffer.read_int()
    speed_growth = buffer.read_int()

    skill1_id = buffer.read_int()
    skill1_unlock = buffer.read_int()
    skill2_id = buffer.read_int()
    skill2_unlock = buffer.read_int()
    skill3_id = buffer.read_int()
    skill3_unlock = buffer.read_int()

    db = get_session()

    try:
        # 🔒 VALIDAÇÃO DE NOME DUPLICADO
        existing = db.query(WarriorTemplate)\
            .filter(WarriorTemplate.name == name)\
            .first()

        if existing and existing.id != warrior_id:
            print("[ADMIN] Nome já existe.")
            return

        if warrior_id == 0:
            warrior = WarriorTemplate()
            db.add(warrior)
        else:
            warrior = db.get(WarriorTemplate, warrior_id)
            if not warrior:
                print("[ADMIN] Warrior não encontrado.")
                return

        warrior.name = name
        warrior.sprite_base  = sprite

        warrior.base_hp = base_hp
        warrior.base_attack = base_attack
        warrior.base_defense = base_defense
        warrior.base_speed = base_speed

        warrior.hp_growth = hp_growth
        warrior.attack_growth = attack_growth
        warrior.defense_growth = defense_growth
        warrior.speed_growth = speed_growth

        warrior.skill1_id = skill1_id
        warrior.skill1_unlock_level = skill1_unlock
        warrior.skill2_id = skill2_id
        warrior.skill2_unlock_level = skill2_unlock
        warrior.skill3_id = skill3_id
        warrior.skill3_unlock_level = skill3_unlock

        db.commit()

        print(f"[ADMIN] Warrior {name} salvo com sucesso.")
        handle_request_warrior_templates(client,buffer)
    except Exception as e:
        print("[ADMIN ERROR]", e)
        db.rollback()

    finally:
        db.close()
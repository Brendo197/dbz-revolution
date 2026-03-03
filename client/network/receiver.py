from protocol.opcodes import *
from protocol.buffer import Buffer
from game.session import session
from network.handle import *

import time


# ==========================================
# CALLBACKS (setados pelas telas)
# ==========================================

login_callback = None
register_step1_callback = None
register_step2_callback = None


def _safe_callback(cb, value):
    try:
        if cb:
            cb(value)
    except Exception as e:
        print("[CALLBACK ERROR]", e)


# ==========================================
# HANDLE PACKET
# ==========================================

def handle_packet(client_socket, data: bytes):
    global login_callback, register_step1_callback, register_step2_callback

    try:
        if not data or len(data) < 1:
            print("[CLIENT] Pacote vazio recebido")
            return

        buffer = Buffer(data)

        try:
            opcode = buffer.read_byte()
        except Exception as e:
            print("[CLIENT] Erro lendo opcode:", e)
            return

        # ======================================
        # SYSTEM
        # ======================================

        if opcode == S_PONG:
            session.server_online = True
            session.last_pong = time.time()
            return

        # ======================================
        # LOGIN
        # ======================================

        elif opcode == S_LOGIN_OK:
            try:
                session.account_id = buffer.read_int()
                session.nickname = buffer.read_string()
                session.is_admin = buffer.read_byte()
                session.has_character = buffer.read_byte() == 1

                if not session.has_character:
                    session.logged_in = True

                    if login_callback:
                        cb = login_callback
                        login_callback = None
                        _safe_callback(cb, True)
                    return

                session.level = buffer.read_int()
                session.exp = buffer.read_int()
                session.bank_zeny = buffer.read_int()
                session.sprite = buffer.read_int()
                session.wins = buffer.read_int()
                session.loses = buffer.read_int()
                session.vip_days = buffer.read_int()

                session.logged_in = True

                if login_callback:
                    cb = login_callback
                    login_callback = None
                    _safe_callback(cb, True)

            except Exception as e:
                print("[CLIENT] Erro processando S_LOGIN_OK:", e)

        elif opcode == S_LOGIN_FAIL:
            try:

                reason = buffer.read_byte()

                message = buffer.read_string()

                session.login_error = message

                if login_callback:
                    cb = login_callback

                    login_callback = None

                    _safe_callback(cb, False)


            except Exception as e:

                print("[CLIENT] Erro processando S_LOGIN_FAIL:", e)
        # ======================================
        # REGISTER STEP 1
        # ======================================

        elif opcode == S_REGISTER_OK_STEP1:
            if register_step1_callback:
                cb = register_step1_callback
                register_step1_callback = None
                _safe_callback(cb, True)

        # ======================================
        # REGISTER STEP 2
        # ======================================

        elif opcode == S_REGISTER_OK:
            session.register_success = True

            if register_step2_callback:
                cb = register_step2_callback
                register_step2_callback = None
                _safe_callback(cb, {
                    "success": True
                })

        elif opcode == S_REGISTER_FAIL:
            try:
                reason = buffer.read_byte()
                message = buffer.read_string()

                session.register_error = message

                if register_step2_callback:
                    cb = register_step2_callback
                    register_step2_callback = None
                    _safe_callback(cb, {
                        "success": False,
                        "error": message
                    })

            except Exception as e:
                print("[CLIENT] Erro processando S_REGISTER_FAIL:", e)

        # ======================================
        # CHAT
        # ======================================

        elif opcode == S_CHAT:
            try:
                nickname = buffer.read_string()
                message = buffer.read_string()

                channel = "global"  # por enquanto

                session.chat_messages[channel].append((nickname, message))

                # Se não está na aba ativa → incrementa unread
                if channel != session.active_chat_channel:
                    session.chat_unread[channel] += 1
            except Exception as e:
                print("[CLIENT] Erro processando S_CHAT:", e)

        elif opcode == S_OPEN_ADMIN:
            session.open_admin_flag = True
        # ======================================
        # UNKNOWN OPCODE
        # ======================================

        elif opcode == S_SEND_WARRIOR_TEMPLATES:
            handle_send_warrior_templates(buffer)
        else:
            print(f"[CLIENT] Opcode desconhecido recebido: {opcode}")

    except Exception as e:
        print("[HANDLE_PACKET ERROR]", e)
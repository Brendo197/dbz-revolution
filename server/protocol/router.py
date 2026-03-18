import traceback
from protocol.buffer import Buffer
from protocol.opcodes import *
from handlers.system import handle_ping

import handlers.auth as auth
from core.sessions import sessions
from handlers.auth import (
    handle_save_warrior_template,
    handle_request_warrior_templates,
    handle_open_admin,
    handle_login,
    handle_register_step1,
    handle_register_step2
)
from handlers.sprite import  (handle_request_sprite_project,handle_save_sprite_project,handle_request_sprite_list,handle_create_sprite)
from core.sessions import sessions

def route_packet(client, data: bytes):
    try:
        buffer = Buffer(data)
        opcode = buffer.read_byte()

        print("[SERVER] OPCODE RECEBIDO:", opcode)

        if opcode == C_PING:
            handle_ping(client, buffer)
            return
        elif opcode == C_REQUEST_SPRITE_LIST:

            if not getattr(client, "is_editor", False):
                print("[SECURITY] Sprite list sem permissão")
                return

            handle_request_sprite_list(client, buffer)
            return
        elif opcode == C_EDITOR_LOGIN:

            token = buffer.read_string()

            if token not in sessions:
                client.disconnect()
                return

            data = sessions[token]

            if not data["is_admin"]:
                client.disconnect()
                return

            client.account_id = data["account_id"]
            client.is_admin = True
            client.is_editor = True

            print("Editor autenticado:", client.account_id)

            return
        elif opcode == C_REQUEST_SPRITE_PROJECT:
            handle_request_sprite_project(client, buffer)
            return
        elif opcode == C_CREATE_SPRITE:
            handle_create_sprite(client)
            return
        elif opcode == C_SAVE_SPRITE_PROJECT:
            handle_save_sprite_project(client, buffer)
            return
        elif opcode == C_LOGIN:
            handle_login(client, buffer)
            return

        elif opcode == C_REGISTER_STEP1:
            handle_register_step1(client, buffer)
            return

        elif opcode == C_REGISTER_STEP2:
            handle_register_step2(client, buffer)
            return

        elif opcode == C_CHAT:
            handle_chat(client, buffer)
            return

        elif opcode == C_OPEN_ADMIN:
            handle_open_admin(client)
            return

        elif opcode == C_REQUEST_WARRIOR_TEMPLATES:
            handle_request_warrior_templates(client, buffer)
            return
        elif opcode == C_SAVE_WARRIOR_TEMPLATE:
            handle_save_warrior_template(client, buffer)
            return
        else:
            print("[SERVER] OPCODE DESCONHECIDO:", opcode)

    except Exception as e:
        print("[SERVER] ERRO NO ROUTE_PACKET:")
        traceback.print_exc()
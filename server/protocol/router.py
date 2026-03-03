import traceback
from protocol.buffer import Buffer
from protocol.opcodes import *
from handlers.system import handle_ping
from handlers.auth import (handle_save_warrior_template,handle_request_warrior_templates,handle_open_admin, handle_login, handle_register_step1, handle_register_step2 )


def route_packet(client, data: bytes):
    try:
        buffer = Buffer(data)
        opcode = buffer.read_byte()

        print("[SERVER] OPCODE RECEBIDO:", opcode)

        if opcode == C_PING:
            handle_ping(client, buffer)
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
        else:
            print("[SERVER] OPCODE DESCONHECIDO:", opcode)

    except Exception as e:
        print("[SERVER] ERRO NO ROUTE_PACKET:")
        traceback.print_exc()
import socket
from protocol.buffer import Buffer
from protocol.opcodes import *
from network import receiver


MAX_PACKET_SIZE = 8192

# =========================
# CHAT
# =========================
def send_chat(client_socket, message: str):
    if not message:
        return False

    buffer = Buffer()
    buffer.write_byte(C_CHAT)
    buffer.write_string(message)

    return send_packet(client_socket, buffer)


# =========================
# SEND PACKET BASE
# =========================
def send_packet(client_socket, data):

    if not client_socket:
        print("Socket inválido")
        return False

    try:

        payload = data if isinstance(data, (bytes, bytearray)) else data.get_bytes()

        size = len(payload)

        print("[SEND_PACKET] size:", size)

        if size <= 0 or size > MAX_PACKET_SIZE:
            print("[SEND_PACKET] Tamanho inválido:", size)
            return False

        packet = size.to_bytes(2, "little") + payload

        print("[SEND_PACKET] enviando opcode:", payload[0])

        return client_socket.send(packet)

    except Exception as e:
        print("[SEND_PACKET ERROR]", e)
        return False
# =========================
# LOGIN
# =========================

def send_login(client_socket, login: str, password: str):
    buffer = Buffer()
    buffer.write_byte(C_LOGIN)
    buffer.write_string(login)
    buffer.write_string(password)

    return send_packet(client_socket, buffer)


# =========================
# REGISTER STEP 1
# =========================

def send_register_step1(client_socket, login: str, password: str, password2: str):
    buffer = Buffer()
    buffer.write_byte(C_REGISTER_STEP1)
    buffer.write_string(login)
    buffer.write_string(password)
    buffer.write_string(password2)

    print("[CLIENT] REGISTER STEP1 enviado")

    return send_packet(client_socket, buffer)


# =========================
# REGISTER STEP 2
# =========================

def create_character(client_socket, nickname, warrior_type, callback):
    buffer = Buffer()
    buffer.write_byte(C_REGISTER_STEP2)

    # 🔥 Agora envia apenas o que o servidor espera
    buffer.write_string(nickname)
    buffer.write_string(warrior_type)

    # registra callback
    receiver.register_step2_callback = callback

    print("[CLIENT] REGISTER STEP2 enviado")

    return send_packet(client_socket, buffer)

def send_open_admin_packet(client_socket):
    buffer = Buffer()
    buffer.write_byte(C_OPEN_ADMIN)
    return send_packet(client_socket, buffer)

def request_warrior_list(client_socket):
    buffer = Buffer()
    buffer.write_byte(C_REQUEST_WARRIOR_TEMPLATES)
    return send_packet(client_socket, buffer)
def send_save_warrior_template(sock, data):
    buffer = Buffer()
    buffer.write_byte(C_SAVE_WARRIOR_TEMPLATE)
    print("[CLIENT] SAVE WARRIOR")
    buffer.write_int(data["id"] or 0)
    buffer.write_string(data["name"])
    buffer.write_string(data["sprite"])

    buffer.write_int(int(data["base_hp"] or 0))
    buffer.write_int(int(data["base_attack"] or 0))
    buffer.write_int(int(data["base_defense"] or 0))
    buffer.write_int(int(data["base_speed"] or 0))

    buffer.write_int(int(data["hp_growth"] or 0))
    buffer.write_int(int(data["attack_growth"] or 0))
    buffer.write_int(int(data["defense_growth"] or 0))
    buffer.write_int(int(data["speed_growth"] or 0))

    buffer.write_int(int(data["skill1_id"] or 0))
    buffer.write_int(int(data["skill1_unlock"] or 0))
    buffer.write_int(int(data["skill2_id"] or 0))
    buffer.write_int(int(data["skill2_unlock"] or 0))
    buffer.write_int(int(data["skill3_id"] or 0))
    buffer.write_int(int(data["skill3_unlock"] or 0))

    send_packet(sock, buffer)

def request_sprite_list(sock):

    buffer = Buffer()
    print("[CLIENT] REQUEST SPRITE LIST")
    buffer.write_byte(C_REQUEST_SPRITE_LIST)

    send_packet(sock, buffer)
def request_sprite_project(sock, sprite_id):

    buffer = Buffer()

    buffer.write_byte(C_REQUEST_SPRITE_PROJECT)
    buffer.write_int(sprite_id)

    send_packet(sock, buffer)
def send_save_sprite_project(sock, project):

    buffer = Buffer()

    buffer.write_byte(C_SAVE_SPRITE_PROJECT)

    # id do sprite
    buffer.write_int(project.id)

    order = project.animation_order

    # quantidade de animações
    buffer.write_int(len(order))

    for name in order:

        anim = project.animations[name]

        buffer.write_string(name)

        buffer.write_int(anim.tick)
        buffer.write_byte(1 if anim.loop else 0)

        buffer.write_int(len(anim.frames))

        for f in anim.frames:

            buffer.write_int(f.x)
            buffer.write_int(f.y)
            buffer.write_int(f.w)
            buffer.write_int(f.h)

            buffer.write_int(f.origin_x)
            buffer.write_int(f.origin_y)

            buffer.write_short(int(f.offset_x))
            buffer.write_short(int(f.offset_y))

            # attack frame
            buffer.write_byte(1 if f.attack_frame else 0)

            # tick override
            if f.tick_override is None:
                buffer.write_byte(0)
            else:
                buffer.write_byte(1)
                buffer.write_int(int(f.tick_override))

            # hitboxes
            buffer.write_int(len(f.hitboxes))
            for box in f.hitboxes:
                buffer.write_int(int(box["x"]))
                buffer.write_int(int(box["y"]))
                buffer.write_int(int(box["w"]))
                buffer.write_int(int(box["h"]))

            # hurtboxes
            buffer.write_int(len(f.hurtboxes))
            for box in f.hurtboxes:
                buffer.write_int(int(box["x"]))
                buffer.write_int(int(box["y"]))
                buffer.write_int(int(box["w"]))
                buffer.write_int(int(box["h"]))

    return send_packet(sock, buffer)
def create_sprite(sock):

    buffer = Buffer()

    buffer.write_byte(C_CREATE_SPRITE)

    return send_packet(sock, buffer)
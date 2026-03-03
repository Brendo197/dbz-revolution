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
        return False

    try:
        payload = data if isinstance(data, (bytes, bytearray)) else data.get_bytes()
        size = len(payload)

        if size <= 0 or size > MAX_PACKET_SIZE:
            print("[SEND_PACKET] Tamanho inválido:", size)
            return False

        packet = size.to_bytes(2, "little") + payload

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
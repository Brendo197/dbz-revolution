from protocol.buffer import Buffer
from protocol.opcodes import S_CHAT
from core.protocol import send_packet


def handle_chat(client, buffer: Buffer):
    message = buffer.read_string()

    if not message:
        debug.print_error("[CHAT] Erro na mensagem")
        return

    if len(message) > 120:
        debug.print_error("[CHAT] Erro na mensagem")
        return

    nickname = getattr(client, "nickname", "Unknown")

    # 🔥 cria buffer novo para cada cliente
    for c in client.server.clients:
        out = Buffer()
        out.write_byte(S_CHAT)
        out.write_string(nickname)
        out.write_string(message)

        send_packet(c, out)

    print(f"[CHAT BROADCAST] {nickname}: {message} -> {len(client.server.clients)} players")
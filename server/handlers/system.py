from protocol.buffer import Buffer
from protocol.opcodes import S_PONG
from core.protocol import send_packet


def handle_ping(client, buffer):


    out = Buffer()
    out.write_byte(S_PONG)

    send_packet(client, out)




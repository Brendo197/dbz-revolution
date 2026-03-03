# server/core/protocol.py
from protocol.buffer import Buffer

def send_packet(client, buffer: Buffer):
    data = buffer.get_bytes()
    size = len(data)

    packet = size.to_bytes(2, "little") + data
    client.socket.sendall(packet)

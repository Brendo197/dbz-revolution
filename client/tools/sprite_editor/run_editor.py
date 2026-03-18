import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

sys.path.append(PROJECT_ROOT)

from network.socket_client import ClientSocket
from tools.sprite_editor.editor.sprite_editor import SpriteEditor
from protocol.buffer import Buffer
from protocol.opcodes import C_EDITOR_LOGIN
from network.sender import send_packet


HOST = "127.0.0.1"
PORT = 4000


def editor_login(sock, token):

    buffer = Buffer()

    buffer.write_byte(C_EDITOR_LOGIN)
    buffer.write_string(token)

    send_packet(sock, buffer)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Token não recebido")
        sys.exit()

    token = sys.argv[1]

    client = ClientSocket(HOST, PORT)

    editor_login(client, token)

    SpriteEditor(client)
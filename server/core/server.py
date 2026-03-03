import socket
import time
from protocol.router import route_packet

from core.client import Client
from core.world import World
from handlers.auth import broadcast_system_message

DEBUG = True


from core.logger import logger

def dprint(*args):
    if DEBUG:
        msg = " ".join(str(a) for a in args)
        logger.log(msg)


MAX_PACKET_SIZE = 8192
MAX_BUFFER_SIZE = 16384


class GameServer:
    def __init__(self, host="0.0.0.0", port=4000):
        self.host = host
        self.port = port

        self.clients = []
        self.world = World()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind((self.host, self.port))
        self.socket.listen()

        # non-blocking
        self.socket.setblocking(False)

        dprint(f"[SERVER] Online em {self.host}:{self.port}")

    # ==========================================
    # MAIN LOOP
    # ==========================================

    def run(self):
        dprint("[SERVER] Loop iniciado")

        while True:
            self.accept_clients()
            self.process_clients()
            self.world.update()

            time.sleep(0.01)

    # ==========================================
    # ACCEPT CLIENTS (ACEITA TODOS DISPONÍVEIS)
    # ==========================================

    def accept_clients(self):
        while True:
            try:
                conn, addr = self.socket.accept()
                conn.setblocking(False)

                client = Client(conn, addr)
                client.recv_buffer = bytearray()
                client.server = self  # 🔥 importante
                self.clients.append(client)

                dprint(f"[CONNECT] {addr}")

            except BlockingIOError:
                break

            except Exception as e:
                dprint("[SERVER] Erro ao aceitar conexão:", e)
                break

    # ==========================================
    # PROCESS CLIENTS
    # ==========================================

    def process_clients(self):
        for client in self.clients[:]:

            if not client.connected:
                self.disconnect(client)
                continue

            try:
                try:
                    chunk = client.socket.recv(4096)
                except BlockingIOError:
                    continue

                # cliente desconectou
                if not chunk:
                    dprint("[SERVER] Cliente desconectou:", client.address)
                    self.disconnect(client)
                    continue

                client.recv_buffer.extend(chunk)

                # 🔐 proteção contra buffer infinito
                if len(client.recv_buffer) > MAX_BUFFER_SIZE:
                    dprint("[SERVER] Buffer overflow de", client.address)
                    self.disconnect(client)
                    continue

                # processa múltiplos pacotes
                while len(client.recv_buffer) >= 2:

                    size = int.from_bytes(
                        client.recv_buffer[0:2], "little"
                    )

                    # 🔐 valida tamanho
                    if size <= 0 or size > MAX_PACKET_SIZE:
                        dprint(
                            "[SERVER] Pacote inválido de",
                            client.address,
                            "size:",
                            size
                        )
                        self.disconnect(client)
                        break

                    if len(client.recv_buffer) < 2 + size:
                        break

                    packet = bytes(
                        client.recv_buffer[2:2 + size]
                    )

                    del client.recv_buffer[:2 + size]

                    try:
                        route_packet(client, packet)
                    except Exception as e:
                        dprint(
                            "[SERVER] Erro no route_packet de",
                            client.address,
                            ":",
                            e
                        )
                        self.disconnect(client)
                        break

            except Exception as e:
                dprint(
                    "[SERVER] ERRO REAL ao processar pacote de",
                    client.address,
                    ":",
                    e
                )
                self.disconnect(client)

    # ==========================================
    # DISCONNECT
    # ==========================================

    def disconnect(self, client):
        dprint(f"[DISCONNECT] {client.address}")

        if hasattr(client, "nickname") and client.nickname:

            broadcast_system_message(
                self,
                f"{client.nickname} deslogou."
            )

        try:
            client.close()
        except Exception as e:
            dprint("[SERVER] Erro ao fechar socket:", e)

        try:
            self.world.remove_player(client)
        except Exception as e:
            dprint("[SERVER] Erro ao remover player do mundo:", e)

        if client in self.clients:
            self.clients.remove(client)
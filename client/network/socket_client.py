import socket
import threading
import time

from protocol.buffer import Buffer
from protocol.opcodes import C_PING
from network.receiver import handle_packet
from network.sender import send_packet  # <-- ajuste se necessário
from game.session import session


class ClientSocket:
    def __init__(self, host, port):
        print("[CLIENT] Criando socket...")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 🔐 KeepAlive (evita roteador matar conexão ociosa)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        try:
            self.socket.connect((host, port))
        except Exception as e:
            print("[CLIENT] Falha ao conectar:", e)
            self.connected = False
            self.running = False
            return

        # 🔐 Timeout pequeno para evitar travamento
        self.socket.settimeout(0.5)

        print("[CLIENT] Conectado ao servidor")

        session.server_online = False
        session.last_pong = time.time()

        self.running = True
        self.connected = True
        self.recv_buffer = bytearray()

        # =========================
        # THREAD RECV
        # =========================
        self.recv_thread = threading.Thread(
            target=self.recv_loop,
            daemon=True
        )
        self.recv_thread.start()

        # =========================
        # THREAD PING
        # =========================
        self.ping_thread = threading.Thread(
            target=self.ping_loop,
            daemon=True
        )
        self.ping_thread.start()

    # =========================
    # RECV LOOP
    # =========================

    def recv_loop(self):
        MAX_PACKET_SIZE = 8192

        while self.running:
            try:
                try:
                    data = self.socket.recv(4096)
                except socket.timeout:
                    continue  # normal

                if not data:
                    self._handle_disconnect()
                    break

                self.recv_buffer += data

                while len(self.recv_buffer) >= 2:
                    size = int.from_bytes(self.recv_buffer[:2], "little")

                    # 🔐 Proteção contra corrupção de protocolo
                    if size <= 0 or size > MAX_PACKET_SIZE:
                        print("[CLIENT] Pacote inválido:", size)
                        self._handle_disconnect()
                        return

                    if len(self.recv_buffer) < 2 + size:
                        break

                    packet = bytes(self.recv_buffer[2:2 + size])
                    del self.recv_buffer[:2 + size]

                    handle_packet(self, packet)

            except Exception as e:
                print("[CLIENT] ERRO recv:", e)
                self._handle_disconnect()
                break

    # =========================
    # PING LOOP
    # =========================

    def ping_loop(self):
        while self.running:
            try:
                buffer = Buffer()
                buffer.write_byte(C_PING)

                send_packet(self, buffer)

            except Exception as e:
                print("[PING ERROR]:", e)

            # 🔐 Timeout mais seguro (15s)
            if time.time() - session.last_pong > 15:
                session.server_online = False

            time.sleep(5)  # envia ping a cada 5 segundos

    # =========================
    # SEND
    # =========================

    def send(self, data: bytes):
        if not self.running:
            return False

        try:
            self.socket.sendall(data)
            return True

        except Exception as e:
            print("[CLIENT] ERRO send:", e)
            self._handle_disconnect()
            return False

    # =========================
    # DISCONNECT
    # =========================

    def _handle_disconnect(self):
        if not self.running:
            return

        print("[CLIENT] Desconectado do servidor")

        self.running = False
        self.connected = False
        session.server_online = False

        try:
            self.socket.close()
        except:
            pass

    def close(self):
        self._handle_disconnect()
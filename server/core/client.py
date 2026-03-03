# server/core/client.py

import socket


MAX_PACKET_SIZE = 8192


class Client:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.is_admin = False
        self.connected = True

        # estado do jogo
        self.account = None
        self.character = None
        self.in_game = False

    # =========================
    # SEND
    # =========================

    def send(self, data: bytes):
        if not self.connected:
            return False

        try:
            if not data or len(data) <= 0:
                return False

            if len(data) > MAX_PACKET_SIZE + 2:  # +2 header
                print("[SERVER] Pacote muito grande para enviar:",
                      len(data))
                self.connected = False
                return False

            self.socket.sendall(data)
            return True

        except Exception as e:
            print("[SERVER] Erro ao enviar para", self.address, ":", e)
            self.connected = False
            return False

    # =========================
    # CLOSE
    # =========================

    def close(self):
        if not self.connected:
            return

        self.connected = False

        try:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except:
                pass

            self.socket.close()

        except Exception as e:
            print("[SERVER] Erro ao fechar socket:", e)
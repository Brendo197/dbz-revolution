import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4000


def check_server_status(callback, timeout=1.5):
    """
    Testa se o servidor está online sem travar a UI
    callback(True/False)
    """

    def _check():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((SERVER_HOST, SERVER_PORT))
            s.close()
            callback(True)
        except:
            callback(False)

    threading.Thread(target=_check, daemon=True).start()

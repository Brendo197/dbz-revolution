# server/network/admin.py
import requests
import threading

SERVER_URL = "http://127.0.0.1:2004"


def _async(task):
    threading.Thread(target=task, daemon=True).start()


def get_players(callback):
    def task():
        try:
            r = requests.get(f"{SERVER_URL}/admin/players-online", timeout=5)
            callback(r.json())
        except Exception as e:
            callback({"success": False, "error": str(e)})
    _async(task)


def make_admin(account_id, callback):
    def task():
        try:
            r = requests.post(
                f"{SERVER_URL}/admin/make-admin",
                json={"account_id": account_id},
                timeout=5
            )
            callback(r.json())
        except Exception as e:
            callback({"success": False, "error": str(e)})
    _async(task)


def remove_admin(account_id, callback):
    def task():
        try:
            r = requests.post(
                f"{SERVER_URL}/admin/remove-admin",
                json={"account_id": account_id},
                timeout=5
            )
            callback(r.json())
        except Exception as e:
            callback({"success": False, "error": str(e)})
    _async(task)


def disconnect_player(account_id, callback):
    def task():
        try:
            r = requests.post(
                f"{SERVER_URL}/admin/disconnect",
                json={"account_id": account_id},
                timeout=5
            )
            callback(r.json())
        except Exception as e:
            callback({"success": False, "error": str(e)})
    _async(task)

import tkinter as tk
import requests

SERVER = "http://127.0.0.1:2004"

class AdminTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Button(
            self,
            text="Aplicar migrations",
            command=self.run_migrations,
            width=25
        ).pack(pady=10)

        self.log = tk.Label(self, text="", fg="green")
        self.log.pack()

    def run_migrations(self):
        try:
            r = requests.post(f"{SERVER}/admin/migrate", timeout=5)
            self.log.config(text=r.json().get("message", "OK"))
        except Exception as e:
            self.log.config(text=str(e), fg="red")

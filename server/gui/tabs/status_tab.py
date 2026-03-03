import tkinter as tk
import psutil
import time

class StatusTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.start_time = time.time()

        self.label = tk.Label(self, text="", font=("Consolas", 11), justify="left")
        self.label.pack(anchor="w", padx=10, pady=10)

        self.update_status()

    def update_status(self):
        uptime = int(time.time() - self.start_time)
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        self.label.config(
            text=f"""Servidor: ONLINE
Uptime: {uptime}s
CPU: {cpu}%
RAM: {ram}%"""
        )

        self.after(1000, self.update_status)

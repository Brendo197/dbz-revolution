import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import time

from launcher.server_process import start_server, stop_server
from launcher.log_handler import setup_logging, log_queue


class ServerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DBZ Revolution - Server")
        self.root.geometry("900x600")

        self.text = ScrolledText(self.root, state="disabled")
        self.text.pack(fill="both", expand=True)

        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(fill="x")

        tk.Button(self.btn_frame, text="START", command=self.start).pack(side="left", padx=5)
        tk.Button(self.btn_frame, text="STOP", command=self.stop).pack(side="left", padx=5)
        tk.Button(self.btn_frame, text="EXIT", command=self.exit).pack(side="right", padx=5)

        self.running = False

        setup_logging()
        self.update_logs()

    def start(self):
        if not self.running:
            self.running = True
            start_server()
            self.log("[INFO] Servidor iniciado")

    def stop(self):
        if self.running:
            stop_server()
            self.running = False
            self.log("[INFO] Servidor parado")

    def exit(self):
        self.stop()
        self.root.destroy()

    def log(self, message):
        self.text.configure(state="normal")
        self.text.insert("end", message + "\n")
        self.text.see("end")
        self.text.configure(state="disabled")

    def update_logs(self):
        while not log_queue.empty():
            msg = log_queue.get()
            self.log(msg)
        self.root.after(100, self.update_logs)

    def run(self):
        self.root.mainloop()

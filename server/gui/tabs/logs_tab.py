import tkinter as tk


class LogsTab:
    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        self.text = tk.Text(self.frame, state="disabled", bg="#111", fg="#0f0")
        self.text.pack(fill="both", expand=True)

    def add_log(self, msg):
        self.text.config(state="normal")
        self.text.insert("end", msg + "\n")
        self.text.see("end")
        self.text.config(state="disabled")

import customtkinter as ctk
import psutil
from tkinter import ttk
import tkinter as tk
from database.db import get_session
from database.models.account import Account

ctk.set_appearance_mode("dark")


class ServerPanel:

    def __init__(self, server):
        self.server = server

        self.app = ctk.CTk()
        self.app.title("DBZ Revolution - Server")
        self.app.geometry("1100x700")

        self.selected_client = None

        self.create_top_bar()
        self.create_players_table()
        self.create_logs_area()

        self.update_ui()

        self.app.mainloop()

    # =============================
    # TOP BAR
    # =============================

    def create_top_bar(self):
        frame = ctk.CTkFrame(self.app)
        frame.pack(fill="x", padx=10, pady=10)

        self.lbl_players = ctk.CTkLabel(frame, text="Players: 0")
        self.lbl_players.pack(side="left", padx=20)

        self.lbl_cpu = ctk.CTkLabel(frame, text="CPU: 0%")
        self.lbl_cpu.pack(side="left", padx=20)

        self.lbl_ram = ctk.CTkLabel(frame, text="RAM: 0%")
        self.lbl_ram.pack(side="left", padx=20)

    # =============================
    # PLAYERS TABLE
    # =============================

    def create_players_table(self):
        frame = ctk.CTkFrame(self.app)
        frame.pack(fill="x", padx=10, pady=10)

        columns = ("nickname", "ip", "admin")

        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)

        self.tree.heading("nickname", text="Nickname")
        self.tree.heading("ip", text="IP")
        self.tree.heading("admin", text="Admin")

        self.tree.column("nickname", width=200)
        self.tree.column("ip", width=200)
        self.tree.column("admin", width=100)

        self.tree.pack(side="left", fill="x", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Buttons Frame
        btn_frame = ctk.CTkFrame(self.app)
        btn_frame.pack(pady=10)

        self.btn_kick = ctk.CTkButton(
            btn_frame,
            text="Kick",
            command=self.kick_selected,
            fg_color="red"
        )
        self.btn_kick.pack(side="left", padx=10)

        self.btn_admin = ctk.CTkButton(
            btn_frame,
            text="Tornar Admin",
            command=self.toggle_admin
        )
        self.btn_admin.pack(side="left", padx=10)

    # =============================
    # LOG AREA
    # =============================

    def create_logs_area(self):
        self.log_box = ctk.CTkTextbox(self.app)
        self.log_box.pack(fill="both", expand=True, padx=10, pady=10)

    # =============================
    # UPDATE LOOP
    # =============================

    def update_ui(self):
        # CPU / RAM
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        self.lbl_cpu.configure(text=f"CPU: {cpu}%")
        self.lbl_ram.configure(text=f"RAM: {ram}%")

        # Players
        self.lbl_players.configure(text=f"Players: {len(self.server.clients)}")

        self.refresh_players_table()

        self.app.after(1000, self.update_ui)

    # =============================
    # REFRESH TABLE
    # =============================

    def refresh_players_table(self):
        self.tree.delete(*self.tree.get_children())

        for client in self.server.clients:
            nickname = getattr(client, "nickname", "SemLogin")
            ip = client.address[0]
            admin_status = "SIM" if getattr(client, "is_admin", False) else "NÃO"

            self.tree.insert("", "end", values=(nickname, ip, admin_status))

    # =============================
    # SELECT PLAYER
    # =============================
    def toggle_admin(self):
        if not self.selected_client:
            return

        db = get_session()

        # alterna valor
        new_value = 0 if self.selected_client.is_admin else 1

        # atualiza memória
        self.selected_client.is_admin = new_value

        # atualiza banco
        account = db.query(Account).filter(
            Account.id == self.selected_client.account.id
        ).first()

        if account:
            account.is_admin = new_value
            db.commit()

        db.close()

        self.refresh_players_table()
    def on_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        nickname = values[0]

        # encontra cliente real
        for client in self.server.clients:
            if getattr(client, "nickname", "SemLogin") == nickname:
                self.selected_client = client
                break

    # =============================
    # KICK
    # =============================

    def kick_selected(self):
        if not self.selected_client:
            return

        self.server.disconnect(self.selected_client)
        self.selected_client = None


def start_gui(server):
    ServerPanel(server)
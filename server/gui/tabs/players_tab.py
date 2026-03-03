import tkinter as tk
from tkinter import ttk, messagebox

from network.admin import (
    get_players,
    make_admin,
    remove_admin,
    disconnect_player
)


class PlayersTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(
            self,
            columns=("id", "username", "admin"),
            show="headings"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Usuário")
        self.tree.heading("admin", text="Admin")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Tornar admin", command=self.on_make_admin)
        self.menu.add_command(label="Remover admin", command=self.on_remove_admin)
        self.menu.add_separator()
        self.menu.add_command(label="Desconectar", command=self.on_disconnect)

        self.tree.bind("<Button-3>", self.on_right_click)

        self.selected = None

        self.refresh_players()

    def on_right_click(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return

        self.tree.selection_set(item)
        values = self.tree.item(item, "values")

        self.selected = {
            "id": int(values[0]),
            "username": values[1],
            "admin": values[2] == "Sim"
        }

        self.menu.entryconfig(
            "Tornar admin",
            state="disabled" if self.selected["admin"] else "normal"
        )
        self.menu.entryconfig(
            "Remover admin",
            state="normal" if self.selected["admin"] else "disabled"
        )

        self.menu.tk_popup(event.x_root, event.y_root)

    def on_make_admin(self):
        make_admin(self.selected["id"], lambda r: self.refresh_players())

    def on_remove_admin(self):
        remove_admin(self.selected["id"], lambda r: self.refresh_players())

    def on_disconnect(self):
        if messagebox.askyesno(
            "Desconectar",
            f"Deseja desconectar {self.selected['username']}?"
        ):
            disconnect_player(self.selected["id"], lambda r: None)

    def refresh_players(self):
        def callback(result):
            if not result.get("success"):
                return

            self.tree.delete(*self.tree.get_children())
            for p in result["players"]:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        p["id"],
                        p["username"],
                        "Sim" if p["is_admin"] else "Não"
                    )
                )

        get_players(callback)
        self.after(3000, self.refresh_players)

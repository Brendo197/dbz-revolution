import tkinter as tk
from tkinter import ttk

from gui.tabs.status_tab import StatusTab
from gui.tabs.players_tab import PlayersTab
from gui.tabs.admin_tab import AdminTab

def start_gui():
    root = tk.Tk()
    root.title("DBZ Revolution - Server Panel")
    root.geometry("800x500")
    root.resizable(False, False)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    notebook.add(StatusTab(notebook), text="Status")
    notebook.add(PlayersTab(notebook), text="Players Online")
    notebook.add(AdminTab(notebook), text="Admin")

    root.mainloop()

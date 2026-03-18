import tkinter as tk
from threading import Thread
import subprocess
import sys
import os

from game.session import session

# IMPORT DO SPRITE EDITOR
from tools.sprite_editor.editor.sprite_editor import SpriteEditor


# ================= THEME =================

BG_MAIN = "#1c1c1c"
BG_PANEL = "#242424"
BG_LIST = "#1f1f1f"
TEXT = "#ffffff"
ACCENT = "#3a7cff"

warrior_listbox = None
warrior_cache = {}


# ================= ADMIN WINDOW =================

def open_admin_window():

    def run_window():

        window = tk.Tk()
        window.title("DBZ Revolution - Admin Panel")
        window.geometry("420x300")
        window.resizable(False, False)
        window.configure(bg=BG_MAIN)

        tk.Label(
            window,
            text="ADMIN PANEL",
            font=("Segoe UI", 14, "bold"),
            bg=BG_MAIN,
            fg=TEXT
        ).pack(pady=15)

        def button(text, command=None):
            return tk.Button(
                window,
                text=text,
                width=22,
                bg=ACCENT,
                fg="white",
                relief="flat",
                command=command
            )

        button("Kick Player").pack(pady=5)
        button("Spawn Item").pack(pady=5)
        button("Teleport").pack(pady=5)
        button("Editar Warriors", open_warrior_editor).pack(pady=5)
        button(
            "Sprite Editor",
            lambda: open_sprite_editor(window)
        ).pack(pady=5)

        tk.Button(
            window,
            text="Fechar",
            width=22,
            command=window.destroy
        ).pack(pady=15)

        window.mainloop()

    Thread(target=run_window, daemon=True).start()


# ================= SPRITE EDITOR =================


def open_sprite_editor(root):

    if not session.editor_token:
        print("Token inválido")
        return

    editor_path = os.path.join(
        os.getcwd(),
        "tools",
        "sprite_editor",
        "run_editor.py"
    )
    print("TOKEN RAW:", repr(session.editor_token))
    subprocess.Popen([
        sys.executable,
        editor_path,
        session.editor_token
    ])


# ================= WARRIOR EDITOR =================

def open_warrior_editor():

    global warrior_listbox, warrior_cache

    editor = tk.Toplevel()
    editor.title("Warrior Editor - DBZ Revolution")
    editor.geometry("1150x650")
    editor.resizable(False, False)
    editor.configure(bg=BG_MAIN)

    current_selected_id = {"id": None}
    filtered_ids = []
    is_saving = {"value": False}

    # ================= STATUS BAR =================

    status_var = tk.StringVar()

    status_label = tk.Label(
        editor,
        textvariable=status_var,
        bg="#151515",
        fg="#7CFC00",
        anchor="w"
    )

    status_label.pack(side="bottom", fill="x")

    def set_status(text, color="#7CFC00"):

        status_label.config(fg=color)
        status_var.set(text)

        editor.after(3000, lambda: status_var.set(""))

    # ================= LEFT PANEL =================

    frame_left = tk.Frame(editor, bg=BG_LIST)
    frame_left.pack(side="left", fill="y")

    tk.Label(
        frame_left,
        text="Warriors",
        bg=BG_LIST,
        fg=TEXT,
        font=("Segoe UI", 12, "bold")
    ).pack(pady=10)

    search_var = tk.StringVar()

    search_entry = tk.Entry(
        frame_left,
        textvariable=search_var,
        bg="#2a2a2a",
        fg=TEXT,
        insertbackground="white"
    )

    search_entry.pack(padx=10, pady=(0, 5))

    scrollbar = tk.Scrollbar(frame_left)
    scrollbar.pack(side="right", fill="y")

    warrior_listbox = tk.Listbox(
        frame_left,
        width=30,
        height=30,
        bg=BG_LIST,
        fg=TEXT,
        selectbackground=ACCENT,
        relief="flat",
        yscrollcommand=scrollbar.set
    )

    warrior_listbox.pack(padx=10, pady=5)

    scrollbar.config(command=warrior_listbox.yview)

    # ================= RIGHT PANEL =================

    frame_right = tk.Frame(editor, bg=BG_MAIN)
    frame_right.pack(side="left", fill="both", expand=True, padx=20, pady=10)

    def section(title):

        frame = tk.Frame(frame_right, bg=BG_PANEL)
        frame.pack(fill="x", pady=6)

        tk.Label(
            frame,
            text=title,
            bg=BG_PANEL,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=10, pady=6)

        inner = tk.Frame(frame, bg=BG_PANEL)
        inner.pack(fill="x", padx=10, pady=6)

        return inner

    def single_field(parent, label):

        row = tk.Frame(parent, bg=BG_PANEL)
        row.pack(fill="x", pady=2)

        tk.Label(
            row,
            text=label,
            width=14,
            bg=BG_PANEL,
            fg=TEXT
        ).pack(side="left")

        entry = tk.Entry(row)
        entry.pack(side="left", fill="x", expand=True)

        return entry

    def two_fields(parent, label1, label2):

        row = tk.Frame(parent, bg=BG_PANEL)
        row.pack(fill="x", pady=2)

        tk.Label(row, text=label1, width=10, bg=BG_PANEL, fg=TEXT).pack(side="left")

        e1 = tk.Entry(row, width=8)
        e1.pack(side="left", padx=5)

        tk.Label(row, text=label2, width=10, bg=BG_PANEL, fg=TEXT).pack(side="left")

        e2 = tk.Entry(row, width=8)
        e2.pack(side="left")

        return e1, e2

    basic = section("Basic Info")

    entry_name = single_field(basic, "Name")
    entry_sprite = single_field(basic, "Sprite")

    stats = section("Base Stats")

    entry_base_hp, entry_base_attack = two_fields(stats, "HP", "ATK")
    entry_base_defense, entry_base_speed = two_fields(stats, "DEF", "SPD")

    growth = section("Growth per Level")

    entry_hp_growth, entry_attack_growth = two_fields(growth, "HP+", "ATK+")
    entry_defense_growth, entry_speed_growth = two_fields(growth, "DEF+", "SPD+")

    skills = section("Skills")

    entry_skill1_id, entry_skill1_unlock = two_fields(skills, "Skill1", "Lv")
    entry_skill2_id, entry_skill2_unlock = two_fields(skills, "Skill2", "Lv")
    entry_skill3_id, entry_skill3_unlock = two_fields(skills, "Skill3", "Lv")

    numeric_fields = [
        entry_base_hp,
        entry_base_attack,
        entry_base_defense,
        entry_base_speed,
        entry_hp_growth,
        entry_attack_growth,
        entry_defense_growth,
        entry_speed_growth,
        entry_skill1_id,
        entry_skill1_unlock,
        entry_skill2_id,
        entry_skill2_unlock,
        entry_skill3_id,
        entry_skill3_unlock
    ]

    def only_numbers(entry):

        def validate(P):
            return P.isdigit() or P == ""

        entry.config(
            validate="key",
            validatecommand=(entry.register(validate), "%P")
        )

    for field in numeric_fields:
        only_numbers(field)

    # ================= LIST FILTER =================

    def update_filtered_list():

        nonlocal filtered_ids

        query = search_var.get().lower()

        warrior_listbox.delete(0, tk.END)

        filtered_ids = []

        for w_id, w in warrior_cache.items():

            if query in w["name"].lower():

                filtered_ids.append(w_id)

                warrior_listbox.insert(
                    tk.END,
                    f'{w_id} - {w["name"]}'
                )

    search_var.trace_add("write", lambda *args: update_filtered_list())

    # ================= LOAD SELECTED =================

    def clear_fields():

        for entry in [entry_name, entry_sprite] + numeric_fields:
            entry.delete(0, tk.END)

        current_selected_id["id"] = None

    def load_selected(event):

        if is_saving["value"]:
            return

        selection = warrior_listbox.curselection()

        if not selection:
            return

        warrior_id = filtered_ids[selection[0]]

        warrior = warrior_cache[warrior_id]

        clear_fields()

        current_selected_id["id"] = warrior_id

        entry_name.insert(0, warrior.get("name", ""))
        entry_sprite.insert(0, warrior.get("sprite", ""))

        for field, key in [
            (entry_base_hp, "base_hp"),
            (entry_base_attack, "base_attack"),
            (entry_base_defense, "base_defense"),
            (entry_base_speed, "base_speed"),
            (entry_hp_growth, "hp_growth"),
            (entry_attack_growth, "attack_growth"),
            (entry_defense_growth, "defense_growth"),
            (entry_speed_growth, "speed_growth"),
            (entry_skill1_id, "skill1_id"),
            (entry_skill1_unlock, "skill1_unlock"),
            (entry_skill2_id, "skill2_id"),
            (entry_skill2_unlock, "skill2_unlock"),
            (entry_skill3_id, "skill3_id"),
            (entry_skill3_unlock, "skill3_unlock"),
        ]:
            field.insert(0, warrior.get(key, 0))

    warrior_listbox.bind("<<ListboxSelect>>", load_selected)


# ================= UPDATE LIST =================

def update_warrior_list(warriors):

    global warrior_listbox, warrior_cache

    if warrior_listbox is None:
        return

    warrior_cache.clear()
    warrior_listbox.delete(0, tk.END)

    for w in warriors:

        warrior_cache[w["id"]] = w

        warrior_listbox.insert(
            tk.END,
            f'{w["id"]} - {w["name"]}'
        )
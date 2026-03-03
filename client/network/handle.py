from launcher.ui.admin_panel import update_warrior_list
from game.session import session

def handle_send_warrior_templates(buffer):
    count = buffer.read_int()

    warriors = []

    for _ in range(count):
        w = {
            "id": buffer.read_int(),
            "name": buffer.read_string(),

            "base_hp": buffer.read_int(),
            "base_attack": buffer.read_int(),
            "base_defense": buffer.read_int(),
            "base_speed": buffer.read_int(),

            "hp_growth": buffer.read_int(),
            "attack_growth": buffer.read_int(),
            "defense_growth": buffer.read_int(),
            "speed_growth": buffer.read_int(),

            "skill1_id": buffer.read_int(),
            "skill1_unlock": buffer.read_int(),

            "skill2_id": buffer.read_int(),
            "skill2_unlock": buffer.read_int(),

            "skill3_id": buffer.read_int(),
            "skill3_unlock": buffer.read_int(),

            "sprite": buffer.read_string(),
        }

        warriors.append(w)

    print(f"[CLIENT] Recebidos {len(warriors)} warrior templates")

    session.warrior_templates = warriors
    update_warrior_list(warriors)
from launcher.ui.admin_panel import update_warrior_list
from game.session import session
from tools.sprite_editor.core.sprite_project import SpriteProject
from tools.sprite_editor.core.animation import Animation
from tools.sprite_editor.core.frame import Frame
from tools.sprite_editor.canvas.sprite_canvas import SpriteCanvas
import os
SPRITE_FOLDER = os.path.join("assets", "sprites")

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

def handle_send_sprite_list(buffer):

    count = buffer.read_int()

    sprites = []

    for _ in range(count):

        sprite_id = buffer.read_int()
        name = buffer.read_string()

        sprites.append({
            "id": sprite_id,
            "name": name
        })

    session.sprite_list = sprites

    print("[CLIENT] Sprites recebidas:", len(sprites))

def handle_send_sprite_project(buffer):

    sprite_id = buffer.read_int()

    anim_count = buffer.read_int()

    project = SpriteProject(sprite_id)

    # 🔥 ORDEM
    project.animation_order = []

    for _ in range(anim_count):

        name = buffer.read_string()

        # 🔥 salva ordem
        project.animation_order.append(name)

        tick = buffer.read_int()
        loop = buffer.read_byte() == 1

        anim = Animation(name)
        anim.tick = tick
        anim.loop = loop

        frame_count = buffer.read_int()

        for _ in range(frame_count):

            x = buffer.read_int()
            y = buffer.read_int()
            w = buffer.read_int()
            h = buffer.read_int()

            frame = Frame(x, y, w, h)

            frame.origin_x = buffer.read_int()
            frame.origin_y = buffer.read_int()

            frame.offset_x = buffer.read_short()
            frame.offset_y = buffer.read_short()

            frame.attack_frame = buffer.read_byte() == 1

            has_override = buffer.read_byte() == 1

            if has_override:
                frame.tick_override = buffer.read_int()
            else:
                frame.tick_override = None

            # hitboxes
            hitbox_count = buffer.read_int()

            for _ in range(hitbox_count):

                frame.hitboxes.append({
                    "x": buffer.read_int(),
                    "y": buffer.read_int(),
                    "w": buffer.read_int(),
                    "h": buffer.read_int()
                })

            # hurtboxes
            hurtbox_count = buffer.read_int()

            for _ in range(hurtbox_count):

                frame.hurtboxes.append({
                    "x": buffer.read_int(),
                    "y": buffer.read_int(),
                    "w": buffer.read_int(),
                    "h": buffer.read_int()
                })

            anim.frames.append(frame)

        project.animations[name] = anim

    # 🔥 GARANTE ORDEM (fallback segurança)
    if not project.animation_order:
        project.animation_order = list(project.animations.keys())

    # 🔥 salva no cache
    session.sprite_cache[sprite_id] = project
    session.sprite_project = project
    session.sprite_project_updated = True

    print("[CLIENT] Sprite project carregado:", sprite_id)
    print("[CLIENT] Animation order:", project.animation_order)



def handle_sprite_created(buffer):

    sprite_id = buffer.read_int()

    print("[CLIENT] Nova sprite criada:", sprite_id)

    session.new_sprite_id = sprite_id

    project = SpriteProject(sprite_id)

    session.sprite_project = project
    session.current_sprite_id = sprite_id
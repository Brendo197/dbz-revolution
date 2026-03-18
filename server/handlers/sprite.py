import os
import json
from protocol.buffer import Buffer
from protocol.opcodes import *
from core.protocol import send_packet

SPRITE_FOLDER = "data/sprites"


def handle_request_sprite_list(client, buffer):

    sprites = []

    if not os.path.exists(SPRITE_FOLDER):
        os.makedirs(SPRITE_FOLDER)

    for file in os.listdir(SPRITE_FOLDER):

        if file.endswith(".json"):

            try:
                sprite_id = int(file.replace(".json", ""))
            except:
                continue

            sprites.append({
                "id": sprite_id,
                "name": f"Sprite {sprite_id}"
            })

    response = Buffer()

    response.write_byte(S_SEND_SPRITE_LIST)
    response.write_int(len(sprites))

    for s in sprites:

        response.write_int(s["id"])
        response.write_string(s["name"])

    send_packet(client,response)

    print("[SERVER] Sprite list enviada:", len(sprites))

def handle_request_sprite_project(client, buffer):

    sprite_id = buffer.read_int()

    path = f"data/sprites/{sprite_id}.json"

    if not os.path.exists(path):

        project = {
            "id": sprite_id,
            "animations": {},
            "animation_order": []
        }

    else:

        with open(path, "r") as f:
            project = json.load(f)

    response = Buffer()

    response.write_byte(S_SEND_SPRITE_PROJECT)

    response.write_int(project["id"])

    animations = project.get("animations", {})

    # 🔥 ORDEM (com fallback)
    order = project.get("animation_order", list(animations.keys()))

    response.write_int(len(order))

    for name in order:

        anim = animations.get(name)

        if not anim:
            continue  # segurança

        response.write_string(name)

        response.write_int(anim.get("tick", 0))
        response.write_byte(1 if anim.get("loop", True) else 0)

        frames = anim.get("frames", [])

        response.write_int(len(frames))

        for f in frames:

            response.write_int(f.get("x", 0))
            response.write_int(f.get("y", 0))
            response.write_int(f.get("w", 0))
            response.write_int(f.get("h", 0))

            response.write_int(f.get("origin_x", 0))
            response.write_int(f.get("origin_y", 0))

            # 🔥 segurança contra crash
            ox = max(-32768, min(32767, int(f.get("offset_x", 0))))
            oy = max(-32768, min(32767, int(f.get("offset_y", 0))))

            response.write_short(ox)
            response.write_short(oy)

            # attack frame
            response.write_byte(1 if f.get("attack_frame", False) else 0)

            tick_override = f.get("tick_override")

            if tick_override is None:
                response.write_byte(0)
            else:
                response.write_byte(1)
                response.write_int(int(tick_override))

            # hitboxes
            hitboxes = f.get("hitboxes", [])
            response.write_int(len(hitboxes))

            for box in hitboxes:
                response.write_int(int(box.get("x", 0)))
                response.write_int(int(box.get("y", 0)))
                response.write_int(int(box.get("w", 0)))
                response.write_int(int(box.get("h", 0)))

            # hurtboxes
            hurtboxes = f.get("hurtboxes", [])
            response.write_int(len(hurtboxes))

            for box in hurtboxes:
                response.write_int(int(box.get("x", 0)))
                response.write_int(int(box.get("y", 0)))
                response.write_int(int(box.get("w", 0)))
                response.write_int(int(box.get("h", 0)))

    send_packet(client, response)
def handle_save_sprite_project(client, buffer):

    sprite_id = buffer.read_int()

    anim_count = buffer.read_int()

    animations = {}
    animation_order = []

    for _ in range(anim_count):

        name = buffer.read_string()

        animation_order.append(name)  # 🔥 GUARDA ORDEM

        tick = buffer.read_int()
        loop = buffer.read_byte() == 1

        frame_count = buffer.read_int()

        frames = []

        for _ in range(frame_count):

            frame = {
                "x": buffer.read_int(),
                "y": buffer.read_int(),
                "w": buffer.read_int(),
                "h": buffer.read_int(),

                "origin_x": buffer.read_int(),
                "origin_y": buffer.read_int(),

                "offset_x": buffer.read_short(),
                "offset_y": buffer.read_short(),

                "attack_frame": buffer.read_byte() == 1
            }

            # tick override
            has_override = buffer.read_byte() == 1

            if has_override:
                frame["tick_override"] = buffer.read_int()
            else:
                frame["tick_override"] = None

            # hitboxes
            hitbox_count = buffer.read_int()
            frame["hitboxes"] = []

            for _ in range(hitbox_count):
                frame["hitboxes"].append({
                    "x": buffer.read_int(),
                    "y": buffer.read_int(),
                    "w": buffer.read_int(),
                    "h": buffer.read_int()
                })

            # hurtboxes
            hurtbox_count = buffer.read_int()
            frame["hurtboxes"] = []

            for _ in range(hurtbox_count):
                frame["hurtboxes"].append({
                    "x": buffer.read_int(),
                    "y": buffer.read_int(),
                    "w": buffer.read_int(),
                    "h": buffer.read_int()
                })

            frames.append(frame)

        animations[name] = {
            "tick": tick,
            "loop": loop,
            "frames": frames
        }

    # 🔥 PROJETO FINAL COM ORDEM
    project = {
        "id": sprite_id,
        "animations": animations,
        "animation_order": animation_order
    }

    os.makedirs("data/sprites", exist_ok=True)

    with open(f"data/sprites/{sprite_id}.json", "w") as f:
        json.dump(project, f, indent=4)

    print(f"[SPRITE SERVER] Sprite {sprite_id} salvo ({len(animations)} animações)")
def handle_create_sprite(client):

    os.makedirs(SPRITE_FOLDER, exist_ok=True)

    ids = []

    for file in os.listdir(SPRITE_FOLDER):

        if file.endswith(".json"):

            try:
                sprite_id = int(file.replace(".json", ""))
                ids.append(sprite_id)
            except:
                pass

    if ids:
        new_id = max(ids) + 1
    else:
        new_id = 1

    project = {
        "id": new_id,
        "animations": {}
    }

    path = f"{SPRITE_FOLDER}/{new_id}.json"

    with open(path, "w") as f:
        json.dump(project, f, indent=4)

    print("[SERVER] Nova sprite criada:", new_id)

    response = Buffer()

    response.write_byte(S_SPRITE_CREATED)
    response.write_int(new_id)

    send_packet(client, response)   # ✔ CORRETO
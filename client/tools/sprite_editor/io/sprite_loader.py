import json
import os
from ..core.sprite_project import SpriteProject, Animation, Frame

PROJECT_FOLDER = "data/sprite_projects"

def load_or_create_project(sprite_id):

    os.makedirs(PROJECT_FOLDER, exist_ok=True)

    path = f"{PROJECT_FOLDER}/{sprite_id}.json"

    if os.path.exists(path):

        return load_sprite(path)

    else:

        project = SpriteProject()

        project.sprite_id = sprite_id
        project.sheet_file = f"assets/sprites/{sprite_id}.png"

        return project

def load_sprite(path):

    if not os.path.exists(path):
        print("Sprite file not found:", path)
        return None

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    project = SpriteProject()

    # -------------------------
    # BASIC DATA (compatível)
    # -------------------------

    project.name = data.get("name", "")
    project.sprite_id = data.get("sprite_id", data.get("id", 0))
    project.sheet_file = data.get("sheet", f"assets/sprites/{project.sprite_id}.png")

    animations = data.get("animations", {})

    # 🔥 ORDEM DAS ANIMAÇÕES
    project.animation_order = data.get(
        "animation_order",
        list(animations.keys())  # fallback
    )

    # -------------------------
    # LOAD ANIMATIONS
    # -------------------------

    for anim_name in project.animation_order:

        anim_data = animations.get(anim_name)

        if not anim_data:
            continue

        animation = Animation(anim_name)

        # compatibilidade (novo + antigo)
        animation.speed = anim_data.get("speed", anim_data.get("tick", 0.08))
        animation.loop = anim_data.get("loop", True)
        animation.pingpong = anim_data.get("pingpong", False)

        frames = anim_data.get("frames", [])

        # -------------------------
        # LOAD FRAMES
        # -------------------------

        for f in frames:

            # suporta dois formatos
            if "rect" in f:
                rect = f.get("rect", [0, 0, 0, 0])
                x, y, w, h = rect
            else:
                x = f.get("x", 0)
                y = f.get("y", 0)
                w = f.get("w", 0)
                h = f.get("h", 0)

            frame = Frame(x, y, w, h)

            # origin
            if "origin" in f:
                origin = f.get("origin", [0, 0])
                frame.origin_x = origin[0]
                frame.origin_y = origin[1]
            else:
                frame.origin_x = f.get("origin_x", 0)
                frame.origin_y = f.get("origin_y", 0)

            # offset
            if "offset" in f:
                offset = f.get("offset", [0, 0])
                frame.offset_x = offset[0]
                frame.offset_y = offset[1]
            else:
                frame.offset_x = f.get("offset_x", 0)
                frame.offset_y = f.get("offset_y", 0)

            # extras
            frame.attack_frame = f.get("attack_frame", False)
            frame.tick_override = f.get("tick_override", None)

            frame.hitboxes = f.get("hitboxes", [])
            frame.hurtboxes = f.get("hurtboxes", [])

            animation.frames.append(frame)

        project.animations[anim_name] = animation

    print("Sprite loaded:", project.sprite_id)
    print("Animation order:", project.animation_order)

    return project
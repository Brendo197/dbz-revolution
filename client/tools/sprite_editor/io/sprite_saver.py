import json

from core.sprite_project import SpriteProject
from core.animation import Animation
from core.frame import Frame
from core.hitbox import Hitbox


def load_project(filepath):

    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    project = SpriteProject(data.get("sprite_id",0))

    project.name = data.get("name","")
    project.sheet = data.get("sheet",None)

    for anim_name, anim_data in data["animations"].items():

        anim = Animation(anim_name)

        anim.speed = anim_data.get("speed",0.1)
        anim.loop = anim_data.get("loop",True)
        anim.pingpong = anim_data.get("pingpong",False)

        for frame_data in anim_data["frames"]:

            x,y,w,h = frame_data["rect"]

            frame = Frame(x,y,w,h)

            origin = frame_data.get("origin",[0,0])
            frame.origin_x = origin[0]
            frame.origin_y = origin[1]

            offset = frame_data.get("offset",[0,0])
            frame.offset_x = offset[0]
            frame.offset_y = offset[1]

            for hb in frame_data.get("hitboxes",[]):

                hitbox = Hitbox(
                    hb["x"],
                    hb["y"],
                    hb["w"],
                    hb["h"],
                    hb.get("type","hit")
                )

                frame.hitboxes.append(hitbox)

            for hb in frame_data.get("hurtboxes",[]):

                hurtbox = Hitbox(
                    hb["x"],
                    hb["y"],
                    hb["w"],
                    hb["h"],
                    hb.get("type","hurt")
                )

                frame.hurtboxes.append(hurtbox)

            anim.frames.append(frame)

        project.animations[anim_name] = anim

    return project
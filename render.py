import bpy
from mathutils import Vector
from math import radians
from random import randint
import os
import json


def set_tracker(tracker, target):
    tracker.select_set(True)
    bpy.ops.object.constraint_add(type='TRACK_TO')
    tracker.constraints["Track To"].target = target
    tracker.constraints["Track To"].up_axis = "UP_Y"
    tracker.constraints["Track To"].track_axis = "TRACK_NEGATIVE_Z"


def render(path, frame, engine="BLENDER_EEVEE", resolution=(512, 512), file_format="PNG", colour_mode="RGB", colour_depth=8):
    sc = bpy.context.scene

    sc.render.filepath = path
    sc.render.engine = engine
    sc.render.resolution_x = resolution[0]
    sc.render.resolution_y = resolution[1]
    sc.render.image_settings.file_format = file_format
    sc.render.image_settings.color_mode = colour_mode
    sc.render.image_settings.color_depth = str(colour_depth)
    sc.render.resolution_percentage = 100
    sc.frame_current = frame

    bpy.context.scene.eevee.use_gtao = True
    bpy.context.scene.eevee.use_ssr = True

    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    with open(r"config\config.json", "r") as json_config:
        config = json.load(json_config)

    with open(r"config\project_tmp.json", "r") as json_project:
        structure = json.load(json_project)

    _, version, _ = bpy.app.version
    blend_retarget = structure["retarget_blend"]
    blend_files = [os.path.join(blend_retarget, file) for file in os.listdir(blend_retarget) if file.endswith(".blend")]

    for blend_file in blend_files:
        bpy.ops.wm.open_mainfile(filepath=blend_file)

        obj = bpy.context.object

        file_name = os.path.splitext(os.path.basename(blend_file))[0]
        bone_anchor = config["render"]["camera bone anchor"]
        armature_name = bpy.data.armatures[0].name
        armature = bpy.data.objects[armature_name]
        bone = armature.pose.bones[bone_anchor]
        bone_rot = bone.matrix.to_euler()
        bone_loc = bone.matrix.to_translation()

        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=bone_loc, rotation=bone_rot)
        camera_offset = Vector((0, 30, 0))
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=camera_offset, rotation=(0, 0, 0))
        empty = bpy.data.objects["Empty"]
        camera = bpy.data.objects["Camera"]
        bpy.data.scenes[0].camera = camera
        camera.parent = empty
        set_tracker(camera, empty)

        bpy.ops.object.select_all(action='DESELECT')

        for obj in (armature, empty):
            obj.select_set(True)
            if obj == armature:
                bpy.context.view_layer.objects.active = armature

        bpy.ops.object.mode_set(mode="POSE")
        armature.data.bones.active = armature.pose.bones[bone_anchor].bone
        bpy.ops.object.parent_set(type='BONE')

        rot_x, rot_y, rot_z = radians(randint(0, 75)), 0, radians(randint(0, 360))
        empty.rotation_euler = (rot_x, rot_y, rot_z)

        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0))

        root = os.path.dirname(__file__)

        render(path         = os.path.join(root, structure['output'], file_name),
               frame        = randint(1, 50),
               resolution   =(config["render"]["x resolution"], config["render"]["y resolution"]),
               engine       = config["render"]["engine"]["workbench"],
               file_format  = config["render"]["format"]["png"],
               colour_mode  = config["render"]["colour mode"]["rgb"],
               colour_depth = config["render"]["colour depth"]["8"])

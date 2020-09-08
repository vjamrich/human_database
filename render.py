import bpy
from mathutils import Vector
from math import radians
from random import randint


def set_tracker(tracker, target):
    tracker.select_set(True)
    bpy.ops.object.constraint_add(type='TRACK_TO')
    tracker.constraints["Track To"].target = target
    tracker.constraints["Track To"].up_axis = "UP_Y"
    tracker.constraints["Track To"].track_axis = "TRACK_NEGATIVE_Z"


if __name__ == "__main__":
    obj = bpy.context.object

    bone_name = "Hips"
    armature_name = bpy.data.armatures[0].name
    armature = bpy.data.objects[armature_name]
    bone = armature.pose.bones[bone_name]
    bone_rot = bone.matrix.to_euler()
    bone_loc = bone.matrix.to_translation()

    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=bone_loc, rotation=bone_rot)
    camera_offset = Vector((0, 0, 8))
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=camera_offset, rotation=(0, 0, 0))
    empty = bpy.data.objects["Empty"]
    camera = bpy.data.objects["Camera"]
    camera.parent = empty
    set_tracker(camera, empty)

    bpy.ops.object.select_all(action='DESELECT')

    for obj in (armature, empty):
        obj.select_set(True)
        if obj == armature:
            bpy.context.view_layer.objects.active = armature

    bpy.ops.object.mode_set(mode="POSE")
    armature.data.bones.active = armature.pose.bones[bone_name].bone
    bpy.ops.object.parent_set(type='BONE')

    rot_x, rot_y, rot_z = radians(randint(0, 75)), 0, radians(randint(0, 360))
    empty.rotation_euler = (rot_x, rot_y, rot_z)

import bpy


def toggle_xray(state=True):
    if version >= 80:
        bpy.data.objects[0].show_in_front = state
    else:
        bpy.data.objects[0].show_x_ray = state


def mw_retarget(target):
    obj = bpy.data.objects[0]

    if version >= 80:
        bpy.context.view_layer.objects.active = obj
    else:
        bpy.context.scene.objects.active = obj

    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.mcp.load_and_retarget(filepath=target)


_, version, _ = bpy.app.version
import_path = "exports\\mass0005.dae"
export_path = "exports\\mass0005.blend"
target_path = "CMU Mocap Database\\61\\61_06.bvh"

bpy.ops.wm.read_homefile(use_empty=True)

bpy.ops.wm.collada_import(filepath     = import_path,
                          import_units = True,
                          find_chains  = True)

toggle_xray(True)
mw_retarget(target_path)
bpy.ops.wm.save_mainfile(filepath=export_path)

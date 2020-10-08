import bpy
import json
import os
import glob
import random


def toggle_xray(state=True):
    if version >= 80:
        bpy.data.objects[0].show_in_front = state
    else:
        bpy.data.objects[0].show_x_ray = state


def mw_retarget(target, frames_target):
    fps = bpy.context.scene.render.fps
    frame = min(int((frames_target / 120) * fps), 20)
    obj = bpy.data.objects[0]

    if version >= 80:
        bpy.context.view_layer.objects.active = obj
    else:
        bpy.context.scene.objects.active = obj

    bpy.ops.object.transform_apply(location=True,
                                   rotation=True,
                                   scale   =True)
    bpy.context.scene.McpEndFrame = frame
    bpy.context.scene.frame_end = frame
    bpy.ops.mcp.load_and_retarget(filepath=target)


def get_targets(input_path):
    bvh_files = []
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".bvh"):
                bvh_files.append(os.path.join(root, file))

    return bvh_files


if __name__ == "__main__":
    with open(r"Data\project_tmp.json", "r") as json_project:
        structure = json.load(json_project)

    with open(r"Data\bvh_index.json", "r") as json_targets:
        targets = json.load(json_targets)

    _, version, _ = bpy.app.version
    dae = structure["dae"]

    dae_files = [os.path.abspath(path) for path in glob.glob(dae + "/*.dae")]
    export_path = os.path.abspath(structure["retarget_blend"])

    for dae_file in dae_files:
        name = os.path.splitext(os.path.basename(dae_file))[0]
        export = os.path.join(export_path, name+".blend")

        target_category = random.choice(list(targets))
        target_path, values = random.choice(list(targets[target_category].items()))
        target_name = values["name"]
        target_label = values["label"]
        target_frames = values["frames"]

        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.wm.collada_import(filepath     = dae_file,
                                  import_units = True,
                                  find_chains  = True)
        toggle_xray(True)
        mw_retarget(target        = target_path,
                    frames_target = target_frames)
        bpy.ops.wm.save_mainfile(filepath=export)

        with open(os.path.join(structure["labels"], name+"_attributes.json"), "r") as json_attributes:
            attributes = json.load(json_attributes)

        attributes["target_name"] = target_name
        attributes["target_category"] = target_category
        attributes["target_label"] = target_label

        with open(os.path.join(structure["labels"], name+"_attributes.json"), "w") as json_attributes:
            json.dump(attributes, json_attributes, indent=4)

import os
import json


def run_blender_headless(blender_path, script_path):
    cmd = f"\"{blender_path}\" --background --python {script_path}"
    os.system(cmd)


if __name__ == "__main__":
    with open(r"config\config.json", "r") as json_config:
        config = json.load(json_config)

    if config["run headless"]["retarget"]:
        run_blender_headless(blender_path = config["software"]["blender 2.79 location"],
                             script_path  = r"retarget.py")

    if config["run headless"]["measure"]:
        run_blender_headless(blender_path = config["software"]["blender 2.83 location"],
                             script_path  = r"get_attributes_from_blend.py")

    if config["run headless"]["render"]:
        run_blender_headless(blender_path = config["software"]["blender 2.83 location"],
                             script_path  = r"render.py")

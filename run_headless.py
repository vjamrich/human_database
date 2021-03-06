import os
import json
import glob
from labels_to_csv import export_to_csv


def run_blender_headless(blender_path, script_path):
    cmd = f"\"{blender_path}\" --background --python {script_path}"
    os.system(cmd)


if __name__ == "__main__":
    with open(r"config\config.json", "r") as json_config:
        config = json.load(json_config)

    with open(r"Data\project_tmp.json", "r") as json_project:
        structure = json.load(json_project)

    if config["run headless"]["retarget"]:
        run_blender_headless(blender_path = config["software"]["blender 2.79 location"],
                             script_path  = r"retarget.py")

    if config["run headless"]["measure"]:
        run_blender_headless(blender_path = config["software"]["blender 2.83 location"],
                             script_path  = r"get_attributes_from_blend.py")

    if config["run headless"]["render"]:
        run_blender_headless(blender_path = config["software"]["blender 2.83 location"],
                             script_path  = r"render.py")

    # labels = os.path.abspath(structure["labels"])
    # attribs_files = [os.path.join(labels, file) for file in os.listdir(labels) if file.endswith(".json")]
    attribs_files = [os.path.abspath(path) for path in glob.glob(fr"{structure['labels']}/*.json")]
    export_path = os.path.join(structure["labels"], "labels.csv")
    export_to_csv(path  = export_path,
                  files = attribs_files)

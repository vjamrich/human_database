import os
import json
import shutil
from datetime import datetime
import pathlib


def create(root_directory = pathlib.Path(__file__).parent, input_mhm =r"Input_mhm"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    structure = {"root"          : fr"{timestamp}",
                 "dae_faces"     : fr"{timestamp}\Input\Input_dae\clothesHideFaces_False",
                 "dae"           : fr"{timestamp}\Input\Input_dae\clothesHideFaces_True",
                 "mhm_faces"     : fr"{timestamp}\Input\Input_mhm\clothesHideFaces_False",
                 "mhm"           : fr"{timestamp}\Input\Input_mhm\clothesHideFaces_True",
                 "retarget_blend": fr"{timestamp}\Input\Retarget_blend",
                 "material_blend": fr"{timestamp}\Input\Material_blend",
                 "labels"        : fr"{timestamp}\Export\Labels",
                 "output"        : fr"{timestamp}\Export\Output"}

    directories = {key: os.path.join(root_directory, value) for key, value in structure.items()}

    for path in directories.values():
        if not os.path.exists(path):
            os.makedirs(path)

    copy_mhm(source=input_mhm, destination=directories["mhm"])
    return directories


def copy_mhm(source, destination):
    files = os.listdir(source)

    for file in files:
        path = os.path.join(source, file)
        if os.path.isfile(path):
            shutil.copy(path, destination)


def export(path, structure):
    with open(os.path.join(path, "project_tmp.json"), "w") as json_project:
        json.dump(structure, json_project, indent=4)


def get(path):
    with open(path, "r") as json_project:
        structure = json.load(json_project)

    return structure


if __name__ == "__main__":
    paths = create(root_directory=r"Data", input_mhm=r"Input_mhm")
    for p in paths:
        print(p)

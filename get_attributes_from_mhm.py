import os
import json
import fileinput
from os.path import basename, splitext
from datetime import datetime


def get_mods(path):
    with open(path, "r") as file:
        f = file
        mods = json.load(f)

    return mods


def get_attributes(path, mods):
    with open(path, "r") as file:
        f = file
        attribs = mods
        attribs = dict(filename=splitext((basename(f.name)))[0], **attribs)

        for line in f:
            for mod in mods:
                if line.find(mod) != -1:
                    attribs[mod] = eval(line[len(mod) + line.find(mod):])

    return attribs


def export_attributes(attribs, path, file_type = "json"):
    suffix = {"json": "attributes",
              "mhm": "showFaces"}

    if "filename" in attribs:
        filename = f"{attribs['filename']}_{suffix[file_type]}.{file_type}"
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_attributes.{file_type}"

    path = os.path.join(path, filename)

    if file_type == "json":
        with open(path, "w") as file:
            f = file
            json.dump(attribs, f, indent=4)

    elif file_type == "mhm":
        header = "# Written by MakeHuman 1.2.0 beta2\n" \
                 "version v1.2.0\n"
        with open(path, "w") as file:
            f = file
            f.write(header)
            for key, value in attribs.items():
                if key == "filename":
                    continue
                f.write(f"modifier {key} {value} \n")

    else:
        raise RuntimeError(f"Invalid file_type. Use json or mhm instead of {file_type}")

    return


def set_flag(path, find, replace):
    with fileinput.FileInput(path, inplace=True) as file:
        f = file
        for line in f:
            print(line.replace(find, replace), end='')

    return


def create_flag(path, flag):
    with open(path, "a") as file:
        f = file
        f.write(flag)

    return


if __name__ == "__main__":
    mods_file = "config/default_modifiers.json"
    mhm_file = "mhm test files\\mass0003.mhm"
    export_file = "mhm test files\\export_attributes.csv"

    modifiers = get_mods(mods_file)
    attributes = get_attributes(mhm_file, modifiers)
    export_attributes(attributes, r".")
    set_flag(mhm_file, "clothesHideFaces True", "clothesHideFaces False")

    for attribute in attributes:
        print(attribute, attributes[attribute])

import csv
import json
import fileinput
from os.path import basename, splitext


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


def export_attributes(attribs, path=None, transpose=True):
    if path is None:
        if "filename" in attribs:
            path = f"{attribs['filename']}.csv"
        else:
            path = "export_attributes.csv"

    with open(path, "w", newline="") as file:
        f = file
        w = csv.writer(f)
        if transpose:
            w.writerows(attribs.items())
        else:
            w.writerow(attribs.keys())
            w.writerow(attribs.values())
        return


def set_flag(path, find, replace):
    with fileinput.FileInput(path, inplace=True) as file:
        f = file
        for line in f:
            print(line.replace(find, replace), end='')
        return


if __name__ == "__main__":
    mods_file = "mhm test files\\default_modifiers.json"
    mhm_file = "mhm test files\\mass0003.mhm"
    export_file = "mhm test files\\export_attributes.csv"

    modifiers = get_mods(mods_file)
    attributes = get_attributes(mhm_file, modifiers)
    export_attributes(attributes)
    set_flag(mhm_file, "clothesHideFaces True", "clothesHideFaces False")

    for attribute in attributes:
        print(attribute, attributes[attribute])

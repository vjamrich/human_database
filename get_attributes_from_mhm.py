import csv
import fileinput
from os.path import basename, splitext


def get_mods(path):
    with open(path, "r") as file:
        f = file
        mods = []
        for line in f:
            mods.append(line.rstrip())
        return mods


def get_attributes(path, mods):
    with open(path, "r") as file:
        f = file
        attribs = dict(filename=splitext((basename(f.name)))[0])
        for line in f:
            for mod in mods:
                if line.find(mod) != -1:
                    attribs[mod] = eval(line[len(mod):])
        return attribs


def export_attributes(path, attribs, transpose=True):
    with open(path, "w") as file:
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
    mods_file = "mhm test files\\mods.txt"
    mhm_file = "mhm test files\\mass0003.mhm"
    export_file = "mhm test files\\export_attributes.csv"

    modifiers = get_mods(mods_file)
    attributes = get_attributes(mhm_file, modifiers)
    export_attributes(export_file, attributes)
    set_flag(mhm_file, "clothesHideFaces True", "clothesHideFaces False")

    for attribute in attributes:
        print(attribute, attributes[attribute])

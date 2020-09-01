import csv
from os.path import basename, splitext


def get_mods(file):
    mods = []
    for line in file:
        mods.append(line.rstrip())
    return mods


def get_attributes(file, mods):
    attribs = dict(filename=splitext((basename(file.name)))[0])
    for line in file:
        for mod in mods:
            if line.find(mod) != -1:
                attribs[mod] = eval(line[len(mod):])
    return attribs


def export_attributes(file, attribs, transpose=True):
    w = csv.writer(file)
    if transpose:
        w.writerows(attribs.items())
    else:
        w.writerow(attribs.keys())
        w.writerow(attribs.values())
    return


if __name__ == "__main__":
    mods_file = open("C:\\HOME\\Python\\human_database\\mhm test files\\mods.txt", "r")
    mhm_file = open("C:\\HOME\\Python\\human_database\\mhm test files\\mass0002.mhm", "r")
    export_file = open("C:\\HOME\\Python\\human_database\\mhm test files\\export_attributes.csv", "w", newline="")

    modifiers = get_mods(mods_file)
    attributes = get_attributes(mhm_file, modifiers)
    export_attributes(export_file, attributes)

    for attribute in attributes:
        print(attribute, attributes[attribute])

    mods_file.close()
    mhm_file.close()
    export_file.close()

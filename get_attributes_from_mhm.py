def get_mods(file):
    mods = []
    for line in file:
        mods.append(line.rstrip())
    return mods


def get_attributes(file, mods):
    attribs = {}
    for line in file:
        for mod in mods:
            if line.find(mod) != -1:
                attribs[mod] = eval(line[len(mod):])
    return attribs


def export_attributes(attribs):
    # TODO
    return


if __name__ == "__main__":
    mods_file = open("C:\\HOME\\Python\\human_database\\mhm test files\\mods.txt", "r")
    mhm_file = open("C:\\HOME\\Python\\human_database\\mhm test files\\mass0002.mhm", "r")

    modifiers = get_mods(mods_file)
    attributes = get_attributes(mhm_file, modifiers)

    for attribute in attributes:
        print(attribute, attributes[attribute])

    mods_file.close()
    mhm_file.close()

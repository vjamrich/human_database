import structure
from get_attributes_from_mhm import *

with open(r"config\config.json", "r") as json_config:
    config = json.load(json_config)

mods_file = config["data"]["modifiers"]
struct = structure.create(root_directory=config["output path"], input_mhm=config["input path"])
mhm_files = [os.path.join(struct["mhm"], file) for file in os.listdir(struct["mhm"])]
modifiers = get_mods(mods_file)

structure.export(path=r"config", structure=struct)

for mhm_file in mhm_files:
    create_flag(path=mhm_file, flag="skeleton cmu_mb.mhskel")
    if config["render"]["subdivide"]:
        set_flag(path=mhm_file, find="subdivide False", replace="subdivide True")
    attributes = get_attributes(path=mhm_file, mods=modifiers)

    export_attributes(attribs   = attributes,
                      path      = struct["labels"],
                      file_type = "json")

    export_attributes(attribs   = attributes,
                      path      = struct["mhm_faces"],
                      file_type = "mhm")

debug = False
if debug:
    for file in mhm_files:
        print(file)
    for mod in modifiers:
        print(mod)

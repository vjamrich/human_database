import structure
from get_attributes_from_mhm import *

with open(r"config\config.json", "r") as json_config:
    config = json.load(json_config)

mods_file = config["data"]["modifiers"]
struct = structure.create(root_directory=config["output path"], input_mhm=config["input path"])
mhm_files = [os.path.join(struct["mhm"], file) for file in os.listdir(struct["mhm"])]
modifiers = get_mods(mods_file)

structure.export(path=r"config", structure=struct)

structure.copy_mhm(source=struct["mhm"], destination=struct["mhm_faces"])
mhm_faces_files = [os.path.join(struct["mhm_faces"], file) for file in os.listdir(struct["mhm_faces"])]
for mhm_faces_file in mhm_faces_files:
    set_flag(mhm_faces_file, find="clothesHideFaces True", replace="clothesHideFaces False")

for mhm_file in mhm_files:
    create_flag(path=mhm_file, flag="skeleton cmu_mb.mhskel")
    attributes = get_attributes(path=mhm_file, mods=modifiers)
    export_attributes(attributes, path=struct["labels"])

debug = False
if debug:
    for file in mhm_files:
        print(file)
    for mod in modifiers:
        print(mod)

# TODO maybe rename faces mhm files to {name}_showFaces

import structure
from get_attributes_from_mhm import *
from index_bvh_files import *

with open(r"config\config.json", "r") as json_config:
    config = json.load(json_config)

mods_file = config["data"]["modifiers"]
struct = structure.create(root_directory=config["output path"], input_mhm=config["input path"])
mhm_files = [os.path.join(struct["mhm"], file) for file in os.listdir(struct["mhm"])]
modifiers = get_mods(mods_file)

structure.export(path=r"Data", structure=struct)

if not mhm_files:
    raise ValueError(".mhm input files not found. Please specify path in config, or generate them using MakeHuman.")

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

bvh_files = get_targets(config["data"]["targets"])

if not bvh_files:
    raise ValueError(".bvh files not found. Please specify path in config, or download them.")

frames_dict = {}
for f in bvh_files:
    frames = get_framerate(f)
    frames_dict[f] = frames

with open(os.path.join(r"Data", "bvh_frames_tmp.json"), "w") as json_bvh:
    json.dump(frames_dict, json_bvh, indent=4)

import os
import json

# MakeHuman won't execute the script properly (for some reason) without declaring variables as global
global root
global mhm
global mhm_faces
global dae
global dae_faces

root = r"D:\HOME\Viktor\Python\human_database"

with open(os.path.join(root, r"data\project_tmp.json"), "r") as json_project:
    structure = json.load(json_project)

mhm = os.path.join(root, structure["mhm"])
mhm_faces = os.path.join(root, structure["mhm_faces"])
dae = os.path.join(root, structure["dae"])
dae_faces = os.path.join(root, structure["dae_faces"])

mhm_files = {os.path.splitext(os.path.basename(file))[0]: os.path.join(root, mhm, file) for file in os.listdir(mhm)}
mhm_faces_files = {os.path.splitext(os.path.basename(file))[0]: os.path.join(root, mhm_faces, file) for file in os.listdir(mhm_faces)}

for file in mhm_files.items():
    name = file[0]
    path = file[1]
    G.app.loadHumanMHM(path)
    gui3d.app.mhapi.exports.exportAsDAE(outputFilename = os.path.join(dae, name+".dae"),
                                        useExportsDir  = False)

for file in mhm_faces_files.items():
    name = file[0]
    path = file[1]
    G.app.loadHumanMHM(path)
    gui3d.app.mhapi.exports.exportAsDAE(outputFilename = os.path.join(dae_faces, name+".dae"),
                                        useExportsDir  = False)

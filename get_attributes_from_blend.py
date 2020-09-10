import bpy
import bmesh
import os
import json


def get_indices(mode=list(bpy.context.tool_settings.mesh_select_mode).index(True)):
    obj = bpy.context.object

    if obj.mode == "EDIT":
        if mode == 2 or mode == "faces":
            indices = [i.index for i in bmesh.from_edit_mesh(obj.data).faces if i.select]
        elif mode == 1 or mode == "edges":
            indices = [i.index for i in bmesh.from_edit_mesh(obj.data).edges if i.select]
        else:
            indices = [i.index for i in bmesh.from_edit_mesh(obj.data).verts if i.select]
    else:
        raise RuntimeError("Edit mode not active")

    return indices


def get_height(object_name, dim="z"):
    obj = bpy.data.objects[object_name]

    if dim == "x" or dim == "X":
        return obj.dimensions.x
    elif dim == "y" or dim == "Y":
        return obj.dimensions.y
    else:
        return obj.dimensions.z


def get_size(indices):
    initial_mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode="EDIT")
    
    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    edges = [e for e in bm.edges]
    length = 0

    for index in indices:
        length += edges[index].calc_length()

    bpy.ops.object.mode_set(mode=initial_mode)

    return length


def get_volume(object_name):
    obj = bpy.data.objects[object_name]
    bm = bmesh.new()

    bm.from_object(obj, bpy.context.evaluated_depsgraph_get())
    volume = bm.calc_volume()
    
    return volume


def get_area(object_name):
    obj = bpy.data.objects[object_name]
    bm = bmesh.new()

    bm.from_object(obj, bpy.context.evaluated_depsgraph_get())
    area = sum(f.calc_area() for f in bm.faces)
    
    return area


if __name__ == "__main__":
    mode_indices = False
    if mode_indices:
        if bpy.context.object.mode == "EDIT":
            print(get_indices())
        quit()

    with open(r"config\indices.json", "r") as json_indices:
        indices = json.load(json_indices)

    with open(r"config\project_tmp.json", "r") as json_project:
        structure = json.load(json_project)

    _, version, _ = bpy.app.version
    dae_faces = structure["dae_faces"]
    dae_faces_files = [os.path.join(dae_faces, file) for file in os.listdir(dae_faces) if file.endswith(".dae")]

    for dae_faces_file in dae_faces_files:
        name = os.path.splitext(os.path.basename(dae_faces_file))[0].split("_")[0]
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.wm.collada_import(filepath=dae_faces_file,
                                  import_units=False)

        with open(os.path.join(structure["labels"], f"{name}_attributes.json"), "r") as json_attributes:
            attributes = json.load(json_attributes)

        obj_name = bpy.data.objects[0].name
        decimals = 2

        bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        for key, value in indices.items():
            attributes[key]  = f"{get_size(value):.{decimals}f}"
        attributes["Height"] = f"{get_height(obj_name):.{decimals}f}"
        attributes["Area"]   = f"{get_area(obj_name):.{decimals}f}"
        attributes["Volume"] = f"{get_volume(obj_name):.{decimals}f}"

        with open(os.path.join(structure["labels"], f"{name}_attributes.json"), "w") as json_attributes:
            json.dump(attributes, json_attributes, indent=4)

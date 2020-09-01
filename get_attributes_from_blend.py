import bpy
import bmesh


def get_indices(mode=list(bpy.context.tool_settings.mesh_select_mode).index(True)):
    obj = bpy.context.object
    indices = []
    
    if obj.mode == "EDIT":
        for _ in bpy.context.active_object.data.edges:
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
    if dim == "x" or dim == "X":
        return bpy.data.objects[object_name].dimensions.x
    elif dim == "y" or dim == "Y":
        return bpy.data.objects[object_name].dimensions.y
    else:
        return bpy.data.objects[object_name].dimensions.z


def get_size(indices):
    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)

    edges = [e for e in bm.edges]
    length = 0

    for edge in edges:
        if edge.index in indices:
            length += edge.calc_length()

    return length


def get_volume():
    bm = bmesh.new()
    bm.from_object(bpy.context.object, bpy.context.evaluated_depsgraph_get())
    volume = bm.calc_volume()
    area = sum(f.calc_area() for f in bm.faces)
    return volume, area


if __name__ == "__main__":
    print("indice size [m]:", get_size(get_indices()))
    print("height [m]:", get_height("Torus"))

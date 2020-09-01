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
    obj = bpy.data.objects[object_name]

    if dim == "x" or dim == "X":
        return round(obj.dimensions.x, 2)
    elif dim == "y" or dim == "Y":
        return round(obj.dimensions.y, 2)
    else:
        return round(obj.dimensions.z, 2)


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


def get_volume(object_name):
    obj = bpy.data.objects[object_name]
    bm = bmesh.new()

    bm.from_object(obj, bpy.context.evaluated_depsgraph_get())
    volume = round(bm.calc_volume(), 2)
    
    return volume


def get_area(object_name):
    obj = bpy.data.objects[object_name]
    bm = bmesh.new()

    bm.from_object(obj, bpy.context.evaluated_depsgraph_get())
    area = round(sum(f.calc_area() for f in bm.faces), 2)
    
    return area


if __name__ == "__main__":
    obj_name = "Cube"

    if bpy.context.object.mode == "EDIT":
        print(f"Indices size [m]: {get_size(get_indices())}")
    print(f"Height [m]: {get_height(obj_name)}")
    print(f"Area [m2]: {get_area(obj_name)}")
    print(f"Volume [m3]: {get_volume(obj_name)}")

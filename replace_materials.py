import bpy


def replace_material(object, target_file, suffix=".001"):
    for slot in object.material_slots:
        old_material_name = slot.material.name
        new_material_name = f"{slot.material.name}{suffix}"
        
        print(old_material_name)
        
        bpy.ops.wm.append(directory = f"{target_file}\\Material\\",
                          filename  = f"{old_material_name}")
        
        if bpy.data.materials.get(new_material_name) is not None:
            print(new_material_name)
            slot.material = bpy.data.materials[new_material_name]
            

if __name__ == "__main__":
    objects = [obj for obj in bpy.data.objects]
    target = r"Data\2020-09-10_10-30-39\Input\Retarget_blend\05_manual_283.blend"

    for obj in objects:
        replace_material(object      = obj,
                         target_file = target)

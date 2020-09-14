import bpy
from mathutils import Vector
from math import radians
from random import randint
import os
import json


def set_tracker(tracker, target):
    tracker.select_set(True)
    bpy.ops.object.constraint_add(type='TRACK_TO')
    tracker.constraints["Track To"].target = target
    tracker.constraints["Track To"].up_axis = "UP_Y"
    tracker.constraints["Track To"].track_axis = "TRACK_NEGATIVE_Z"


def render(path, frame, engine="BLENDER_EEVEE", resolution=(512, 512), file_format="PNG", colour_mode="RGB", colour_depth=8):
    sc = bpy.context.scene

    sc.render.filepath = path
    sc.render.engine = engine
    sc.render.resolution_x = resolution[0]
    sc.render.resolution_y = resolution[1]
    sc.render.image_settings.file_format = file_format
    sc.render.image_settings.color_mode = colour_mode
    sc.render.image_settings.color_depth = str(colour_depth)
    if colour_mode == "RGBA":
        sc.render.film_transparent = True
    else:
        sc.render.film_transparent = False
    sc.render.resolution_percentage = 100
    sc.frame_current = frame

    sc.view_layers[0].use_pass_normal = True
    sc.view_layers[0].use_pass_z = True

    bpy.context.scene.eevee.use_gtao = True
    bpy.context.scene.eevee.use_ssr = True

    bpy.ops.render.render(write_still=True)


def replace_material(target_file, suffix=".001"):
    objects = [obj for obj in bpy.data.objects]
    for obj in objects:
        for slot in obj.material_slots:
            old_material_name = slot.material.name
            new_material_name = f"{slot.material.name}{suffix}"

            bpy.ops.wm.append(directory=f"{target_file}\\Material\\",
                              filename=f"{old_material_name}")

            if bpy.data.materials.get(new_material_name) is not None:
                slot.material = bpy.data.materials[new_material_name]


def delete_all():
    objs = bpy.data.objects
    for obj in objs:
        objs.remove(obj, do_unlink=True)


def protect_materials():
    materials = bpy.data.materials

    for mat in materials:
        mat.use_fake_user = True


def set_render_settings():
    # world colour
    bpy.context.scene.render.film_transparent = True

    # ambient occlusion
    bpy.context.scene.eevee.use_gtao = True

    # ss reflections
    bpy.context.scene.eevee.use_ssr = True

    # shadows
    bpy.context.scene.eevee.shadow_cascade_size = '1024'
    bpy.context.scene.eevee.shadow_cube_size = '1024'
    bpy.context.scene.eevee.use_soft_shadows = True


# add HDRI
def set_world(image_path, strength):
    if bpy.data.scenes[0].world is None:
        bpy.ops.world.new()
        bpy.data.scenes[0].world = bpy.data.worlds[0]

    world = bpy.data.scenes[0].world

    node_tree = world.node_tree
    world.use_nodes = True

    for node in node_tree.nodes:
        if node.type == "BACKGROUND":
            background = node
            background.inputs["Strength"].default_value = strength

    tex_environment = node_tree.nodes.new(type="ShaderNodeTexEnvironment")
    tex_environment.image = bpy.data.images.load(image_path)

    links = node_tree.links
    links.new(tex_environment.outputs["Color"], background.inputs["Color"])


# alpha materials
def set_alpha():
    for mat in bpy.data.materials:
        node_tree = mat.node_tree
        if not node_tree:
            continue

        if mat.name_full[:4] == "Eye_":
            mat.show_transparent_back = True
        else:
            mat.show_transparent_back = False
        mat.use_backface_culling = True
        mat.use_screen_refraction = True
        mat.blend_method = 'HASHED'
        mat.shadow_method = 'OPAQUE'

        tex_image = bsdf = None
        for node in node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                tex_image = node
            elif node.type == 'BSDF_PRINCIPLED':
                bsdf = node

        if not (tex_image and bsdf):
            continue

        links = node_tree.links
        links.new(tex_image.outputs["Alpha"], bsdf.inputs["Alpha"])


def output_passes(path, *args):
    bpy.context.scene.use_nodes = True

    scene = bpy.data.scenes[0]
    node_tree = scene.node_tree
    render_layers = node_tree.nodes["Render Layers"]

    for output_pass in args:
        file_output = node_tree.nodes.new(type="CompositorNodeOutputFile")
        file_output.base_path = path
        file_output.file_slots[0].path = output_pass

        links = node_tree.links

        if output_pass == "Depth":
            normalize = node_tree.nodes.new(type="CompositorNodeNormalize")
            links.new(render_layers.outputs[output_pass], normalize.inputs[0])
            links.new(normalize.outputs[0], file_output.inputs[0])
        else:
            links.new(render_layers.outputs[output_pass], file_output.inputs[0])


if __name__ == "__main__":
    with open(r"config\config.json", "r") as json_config:
        config = json.load(json_config)

    with open(r"config\project_tmp.json", "r") as json_project:
        structure = json.load(json_project)

    _, version, _ = bpy.app.version
    blend_retarget = os.path.abspath(structure["retarget_blend"])
    blend_files = [os.path.join(blend_retarget, file) for file in os.listdir(blend_retarget) if file.endswith(".blend")]
    dae = os.path.abspath(structure["dae"])
    dae_files = [os.path.join(dae, file) for file in os.listdir(dae) if file.endswith(".dae")]

    for dae_file in dae_files:
        export_path = os.path.abspath(structure["material_blend"])
        name = os.path.splitext(os.path.basename(dae_file))[0]
        export = os.path.join(export_path, name+".blend")

        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.wm.collada_import(filepath=dae_file)
        protect_materials()
        delete_all()
        bpy.ops.wm.save_mainfile(filepath=export)

    for blend_file in blend_files:
        bpy.ops.wm.open_mainfile(filepath=blend_file)

        obj = bpy.context.object

        file_name = os.path.splitext(os.path.basename(blend_file))[0]
        replace_material(os.path.join(structure["material_blend"], file_name + ".blend"))

        bone_anchor = config["render"]["camera bone anchor"]
        armature_name = bpy.data.armatures[0].name
        armature = bpy.data.objects[armature_name]
        bone = armature.pose.bones[bone_anchor]
        bone_rot = bone.matrix.to_euler()
        bone_loc = bone.matrix.to_translation()

        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=bone_loc, rotation=bone_rot)
        camera_offset = Vector((0, 35, 0))
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=camera_offset, rotation=(0, 0, 0))
        empty = bpy.data.objects["Empty"]
        camera = bpy.data.objects["Camera"]
        bpy.data.scenes[0].camera = camera
        camera.parent = empty
        set_tracker(camera, empty)

        bpy.ops.object.select_all(action='DESELECT')

        for obj in (armature, empty):
            obj.select_set(True)
            if obj == armature:
                bpy.context.view_layer.objects.active = armature

        bpy.ops.object.mode_set(mode="POSE")
        armature.data.bones.active = armature.pose.bones[bone_anchor].bone
        bpy.ops.object.parent_set(type='BONE')

        rot_x, rot_y, rot_z = radians(randint(0, 0)), 0, radians(randint(180, 180))
        empty.rotation_euler = (rot_x, rot_y, rot_z)

        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0))

        root = os.path.dirname(__file__)

        image_path = r"D:\HOME\Viktor\Python\human_database\paul_lobe_haus_1k.hdr"

        set_world(image_path, strength=0.4)
        set_alpha()
        set_render_settings()

        render(path         = os.path.join(root, structure['output'], file_name),
               frame        = randint(1, 50),
               resolution   =(config["render"]["x resolution"], config["render"]["y resolution"]),
               engine       = config["render"]["engine"],
               file_format  = config["render"]["format"],
               colour_mode  = config["render"]["colour mode"],
               colour_depth = config["render"]["colour depth"])

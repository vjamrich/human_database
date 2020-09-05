import os

blender_280_loc = "\"C:\\Program Files\\Blender Foundation\\Blender 2.83\\blender.exe\""
blender_279_loc = "\"blender-2.79b-windows64\\blender.exe\""

script_loc = "retarget.py"
cmd = f"{blender_279_loc} --background --python {script_loc}"

os.system(cmd)

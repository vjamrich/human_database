import os


def run_blender_headless(blender_path, script_path):
    cmd = f"\"{blender_path}\" --background --python {script_path}"
    os.system(cmd)


if __name__ == "__main__":
    blender = r"D:\HOME\Viktor\Python\Human db\blender-2.79b-windows64\blender.exe"
    script = r"retarget.py"
    run_blender_headless(blender_path = blender,
                         script_path  = script)

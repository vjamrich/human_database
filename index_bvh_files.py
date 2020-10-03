import csv
import os


def get_targets(input_path):
    bvh_files = []
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".bvh"):
                bvh_files.append(os.path.join(root, file))

    return bvh_files


def get_framerate(path):
    with open(path, "r") as file:
        f = file

        frames_find = "Frames:"
        time_find = "Frame Time:"

        for line in f:
            if line.find(frames_find) != -1:
                frames = eval(line[len(frames_find) + line.find(frames_find):])
                break
            # if line.find(time_find) != -1:
            #     frame_time = eval(line[len(time_find) + line.find(time_find):])

    return frames


def generate_index(frames):
    paths = {}
    for key, value in frames.items():
        name = os.path.splitext(os.path.basename(key))[0]
        paths[name] = {"path": key,
                       "frames": value}

    with open(r"Data/BVH_categories.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        targets = {"Walk": {},
                   "Run": {},
                   "Other": {}}
        for row in csv_reader:
            name, label, category = row
            if name in paths:
                targets[category][paths[name]["path"]] = {"name"    : name,
                                                          "label"   : label,
                                                          "frames"  : paths[name]["frames"]}

    return targets

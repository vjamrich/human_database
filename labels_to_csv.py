import os
import csv
import json


def export_to_csv(path, files):
    with open(r"Data/modifiers_dict.json", "r") as json_mods_dict:
        modifiers_dict = json.load(json_mods_dict)

    csv_file = open(path, "w", newline="")
    csv_writer = csv.writer(csv_file)
    labels = {}
    for json_path in files:
        with open(json_path, "r") as file:
            json_labels = json.load(file)
            for key, value in modifiers_dict.items():
                if key in json_labels:
                    labels.setdefault(modifiers_dict[key], [])
                    labels[modifiers_dict[key]].append(json_labels[key])

    labels_rows = [row for row in map(list, zip(*labels.values()))]
    csv_writer.writerow(labels.keys())
    csv_writer.writerows(labels_rows)

    csv_file.close()


if __name__ == "__main__":
    with open(r"config/project_tmp.json", "r") as json_project:
        structure = json.load(json_project)

    json_1 = r"path.to.labels.json"
    json_2 = r"path.to.labels.json"
    export_path = os.path.join(structure["labels"], r"labels.csv")

    export_to_csv(export_path, json_1, json_2)

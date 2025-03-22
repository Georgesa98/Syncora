import os
import json


def ensure_exists(file_path: str):
    return os.path.exists(file_path)


def read_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
        return data


def write_json_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

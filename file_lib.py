import json


def read_json_file(filepath: str) -> json:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def write_json_file(filepath: str, data: json, mode='w'):
    with open(filepath, mode, encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def write_txt_file(filepath: str, text: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

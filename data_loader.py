from pathlib import Path


def load_data(path: str):
    if (path := Path(path)).exists():
        with open(path, 'r') as data_file: return data_file.read()
    else:
        return None

def write_output(result: str, path):
    with open(path, 'w') as output_file: output_file.write(result)

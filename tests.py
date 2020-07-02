import os
import pickle as pk

def read():
    script_dir = os.path.dirname(__file__)
    rel_path = "tests/sayama/[0.1, 0.0, 0.0, 0.0]"
    abs_file_path = os.path.join(script_dir, rel_path)
    with (open(abs_file_path, 'rb')) as f:
        return pk.load(f)
    
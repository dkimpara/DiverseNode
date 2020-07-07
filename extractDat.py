import os
import pickle as pk

def read_pickle(subpath):
    script_dir = os.path.dirname(__file__)
    rel_path = "tests/" + subpath 
    abs_file_path = os.path.join(script_dir, rel_path)
    with (open(abs_file_path, 'rb')) as f:
        return pk.load(f)
    
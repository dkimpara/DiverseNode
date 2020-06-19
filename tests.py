from pathlib import Path
import os

subdir = "lol"
filename = "yeet.txt"

script_dir = os.path.dirname(__file__)  
rel_path = "tests/" + subdir
abs_dir_path = os.path.join(script_dir, rel_path)
# safely make dir
Path(abs_dir_path).mkdir(parents=True, exist_ok=True)

file_path = '/' + filename

rel_path = "tests/" + subdir + '/' + filename
abs_file_path = os.path.join(script_dir, rel_path)


f = open(abs_file_path, 'w')
f.write("yeeeeet yeet")
f.close()
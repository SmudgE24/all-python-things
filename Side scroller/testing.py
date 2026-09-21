import os

base_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(base_dir, "level1.txt")

f = open(file_path, "x")
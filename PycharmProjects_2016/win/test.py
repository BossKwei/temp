import os


all_dirs = []
for root, dirs, files in os.walk('C:', topdown=False):
    all_dirs.append(root)

pass
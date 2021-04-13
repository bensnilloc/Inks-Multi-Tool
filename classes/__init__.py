import os

for path in ["data", "cookies"]:
    if not os.path.exists(path):
        os.mkdir(path)
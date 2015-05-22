"""Build file."""

import os

OBJ_DIR = "objects"
OBJ_INIT_F = "objects/__init__.py"

obj_fs = []
for f in os.listdir(OBJ_DIR):
    if f.endswith(".py") and f != "__init__.py":
        obj_fs.append("\"{0}\"".format(f[:-3]))

with open(OBJ_INIT_F, 'w') as f:
    f.write("__all__ = [{0}]".format(', '.join(obj_fs)))
#!/usr/bin/python

import os
import sys

from pathlib import Path
path = Path("pwd")
print(path.parent.absolute())

sys.path.append('C:/python/files/folder1')
import os.path as ospath
import sys

current_path = ospath.dirname(ospath.realpath(__file__))
root_path = ospath.dirname(ospath.dirname(current_path))
sys.path.append(root_path)

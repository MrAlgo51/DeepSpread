import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)
import os

# Add the project root to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules import config

print("MEMPOOL_LOG_PATH is:", config.MEMPOOL_LOG_PATH)

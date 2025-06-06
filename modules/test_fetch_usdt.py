import os
import config
import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.fetch_usdt_premium import fetch_usdt_premium

print(fetch_usdt_premium())

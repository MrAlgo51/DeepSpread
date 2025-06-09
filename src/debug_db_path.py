# src/debug_db_path.py
import os
from modules.config import DB_PATH

print("📍 Absolute DB path:", os.path.abspath(DB_PATH))

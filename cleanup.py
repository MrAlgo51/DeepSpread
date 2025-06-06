# cleanup.py

import os
import shutil

# Paths
ROOT = os.path.dirname(__file__)
LOGS_DIR = os.path.join(ROOT, "logs")
TESTS_DIR = os.path.join(ROOT, "tests")

# Cleanup targets
junk_files = [
    os.path.join(ROOT, "data", "deepspread.db"),
    os.path.join(ROOT, "deepspread.db"),
]

pyc_extensions = [".pyc"]

# Remove old DBs
for f in junk_files:
    if os.path.isfile(f):
        print(f"🗑️ Deleting {f}")
        os.remove(f)

# Move test files to /tests
os.makedirs(TESTS_DIR, exist_ok=True)
for file in os.listdir(ROOT):
    if file.startswith("test_") and file.endswith(".py"):
        src = os.path.join(ROOT, file)
        dst = os.path.join(TESTS_DIR, file)
        print(f"📦 Moving {file} to tests/")
        shutil.move(src, dst)

# Delete .pyc files and __pycache__
for root, dirs, files in os.walk(ROOT):
    for file in files:
        if any(file.endswith(ext) for ext in pyc_extensions):
            fpath = os.path.join(root, file)
            print(f"🧹 Removing compiled file: {fpath}")
            os.remove(fpath)
    for dir in dirs:
        if dir == "__pycache__":
            dpath = os.path.join(root, dir)
            try:
                print(f"🧨 Removing __pycache__ directory: {dpath}")
                shutil.rmtree(dpath)
            except PermissionError:
                print(f"⚠️ Skipped locked __pycache__: {dpath}")

print("✅ Cleanup complete.")

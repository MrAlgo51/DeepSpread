import config
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.error_logger import log_error, log_to_file

# Test the error logger
log_error("log_test", "This is a test of the error logger.")

# Test the general logger
log_to_file("log_test", "This is a test of the general file logger.")

print("✅ Test log entries written. Check the 'logs' folder.")

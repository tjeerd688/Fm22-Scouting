import subprocess
from subprocess import call
import os
from pathlib import Path

# Path to the script you want to run
path = Path("..") /"FM22"/ "Main Script" / "Main.py"
script_path = str(path)

try:
    # Run the script using subprocess
    result = call(["python", script_path])
    # Check the output
    print("Subprocess stdout:", result.stdout)
    print("Subprocess stderr:", result.stderr)

except subprocess.CalledProcessError as e:
    # Handle subprocess errors
    print(f"Subprocess error: {e}")
except Exception as e:
    # Handle other exceptions
    print(f"An error occurred: {e}")

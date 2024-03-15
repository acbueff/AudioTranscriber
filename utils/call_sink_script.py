import subprocess
import sys
import platform

def call_script(script_name):
    """Call the given Python script using a subprocess."""
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")

if __name__ == "__main__":
    os_name = platform.system()

    if os_name == "Windows":
        call_script("windows.py")
    elif os_name == "Linux":
        call_script("linux.py")
    else:
        print(f"Unsupported operating system: {os_name}")
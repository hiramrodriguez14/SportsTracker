import os
import sys
import subprocess

def setup_and_activate_venv():
    workspace_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    venv_path = os.path.join(workspace_path, ".venv")
    requirements_file = os.path.join(workspace_path, "requirements.txt")

    if sys.prefix == venv_path:
        print("Virtual environment already activated.")
        return

    if not os.path.exists(venv_path):
        print("Virtual environment not found. Creating one...")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

    if sys.platform == "win32":
        python_exec = os.path.join(venv_path, "Scripts", "python.exe")
        pip_exec = os.path.join(venv_path, "Scripts", "pip.exe")
        activate_script = os.path.join(venv_path, "Scripts", "Activate.ps1")
    else:
        python_exec = os.path.join(venv_path, "bin", "python")
        pip_exec = os.path.join(venv_path, "bin", "pip")
        activate_script = os.path.join(venv_path, "bin", "activate")

    if not os.path.exists(pip_exec):
        print("pip not found in virtual environment. Installing pip...")
        subprocess.run([sys.executable, "-m", "ensurepip", "--default-pip"], check=True)

    if os.path.exists(requirements_file):
        print("Installing dependencies from requirements.txt...")
        subprocess.run([python_exec, "-m", "pip", "install", "-r", requirements_file, "--break-system-packages"], check=True)

    if "VIRTUAL_ENV" not in os.environ:
        print("Virtual environment setup complete. You may need to restart manually.")
        sys.exit(0)

    print(f"To activate manually later, run:\nsource {activate_script}" if sys.platform != "win32" else f"& {activate_script}")

setup_and_activate_venv()

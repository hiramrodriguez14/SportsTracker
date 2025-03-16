import os
import sys
import subprocess

def setup_and_activate_venv():
    venv_path = os.path.join(os.getcwd(), ".venv")
    requirements_file = os.path.join(os.getcwd(), "requirements.txt")

    if sys.prefix == venv_path:
        print("Virtual environment already activated.")
        return  

    if not os.path.exists(venv_path):
        print("Virtual environment not found. Creating one...")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

    if sys.platform == "win32":
        python_exec = os.path.join(venv_path, "Scripts", "python.exe")
        pip_exec = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        python_exec = os.path.join(venv_path, "bin", "python")
        pip_exec = os.path.join(venv_path, "bin", "pip")

    if not os.path.exists(pip_exec):
        print("pip not found in virtual environment. Installing pip...")
        subprocess.run([sys.executable, "-m", "ensurepip", "--default-pip"], check=True)

    if os.path.exists(requirements_file):
        print("Installing dependencies from requirements.txt...")
        subprocess.run([python_exec, "-m", "pip", "install", "-r", requirements_file, "--break-system-packages"], check=True)

    if "VIRTUAL_ENV" not in os.environ:
        print("Restarting script inside virtual environment...")
        os.execv(python_exec, [python_exec] + sys.argv)

setup_and_activate_venv()

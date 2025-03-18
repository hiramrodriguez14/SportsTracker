import os
import sys
import subprocess

def setup_and_activate_venv():
    workspace_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get the workspace root
    venv_path = os.path.join(workspace_path, "venv")
    requirements_file = os.path.join(workspace_path, "requirements.txt")

    # Check if already inside venv
    if sys.prefix == venv_path:
        print("✅ Virtual environment already activated.")
        return  

    # Create venv if not found
    if not os.path.exists(venv_path):
        print("⚠️ Virtual environment not found. Creating one...")
        subprocess.run(["C:\\Users\\proli\\AppData\\Local\\Programs\\Python\\Python313\\python.exe", "-m", "venv", venv_path], check=True)

    # Determine correct Python executable
    if sys.platform == "win32":
        activate_script = os.path.join(venv_path, "Scripts", "Activate.ps1")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")

    # Install dependencies if requirements.txt exists
    if os.path.exists(requirements_file):
        print("📦 Installing dependencies from requirements.txt...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file, "--break-system-packages"], check=True)

    # Auto-activate virtual environment
    if sys.platform == "win32":
        print(f"🔄 To activate, run: & {activate_script}")
    else:
        print(f"🔄 To activate, run: source {activate_script}")

setup_and_activate_venv()

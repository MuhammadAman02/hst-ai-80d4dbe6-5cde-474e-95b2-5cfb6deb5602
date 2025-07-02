import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version meets requirements."""
    required_version = (3, 8)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"Error: Python {required_version[0]}.{required_version[1]} or higher is required.")
        print(f"Current version: {current_version[0]}.{current_version[1]}")
        return False
    return True

def create_virtual_environment():
    """Create a virtual environment if it doesn't exist."""
    venv_dir = Path("venv")
    
    if venv_dir.exists():
        print(f"Virtual environment already exists at {venv_dir}")
        return True
        
    try:
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        print(f"Virtual environment created at {venv_dir}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False

def get_venv_python_path():
    """Get the path to the Python executable in the virtual environment."""
    if platform.system() == "Windows":
        return Path("venv/Scripts/python.exe")
    return Path("venv/bin/python")

def get_venv_pip_path():
    """Get the path to the pip executable in the virtual environment."""
    if platform.system() == "Windows":
        return Path("venv/Scripts/pip.exe")
    return Path("venv/bin/pip")

def install_dependencies():
    """Install dependencies using pip."""
    pip_path = get_venv_pip_path()
    
    if not pip_path.exists():
        print(f"Error: pip not found at {pip_path}")
        return False
        
    try:
        print("Installing dependencies...")
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        print("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def verify_critical_dependencies():
    """Verify that critical dependencies are installed and available."""
    python_path = get_venv_python_path()
    
    if not python_path.exists():
        print(f"Error: Python not found at {python_path}")
        return False
        
    # Check for critical modules
    critical_modules = ["uvicorn", "fastapi", "nicegui", "pydantic"]
    missing_modules = []
    
    for module in critical_modules:
        try:
            result = subprocess.run(
                [str(python_path), "-c", f"import {module}; print('{module} found')"], 
                capture_output=True, 
                text=True
            )
            if f"{module} found" not in result.stdout:
                missing_modules.append(module)
        except subprocess.CalledProcessError:
            missing_modules.append(module)
    
    if missing_modules:
        print("Error: The following critical modules were not found:")
        for module in missing_modules:
            print(f"  - {module}")
        return False
            
    return True

def print_activation_instructions():
    """Print instructions for activating the virtual environment."""
    if platform.system() == "Windows":
        print("\nTo activate the virtual environment, run:")
        print("    venv\\Scripts\\activate")
    else:
        print("\nTo activate the virtual environment, run:")
        print("    source venv/bin/activate")
    
    print("\nAfter activation, you can run the application with:")
    print("    python main.py")

def main():
    """Main setup function."""
    if not check_python_version():
        return 1
        
    if not create_virtual_environment():
        return 1
        
    if not install_dependencies():
        return 1
        
    if not verify_critical_dependencies():
        print("\nSome critical dependencies could not be verified.")
        print("Please try running the following commands manually:")
        print(f"    {get_venv_pip_path()} install -r requirements.txt")
        return 1
        
    print_activation_instructions()
    return 0

if __name__ == "__main__":
    sys.exit(main())
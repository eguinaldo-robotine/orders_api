#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, check=True):
    print(f"Executando: {command}")
    result = subprocess.run(command, shell=True, check=check)
    return result.returncode == 0


def run_tests():
    project_root = Path(__file__).parent.parent
    venv_path = project_root / ".venv"
    
    print("=" * 60)
    print("Executando testes")
    print("=" * 60)
    
    pytest_cmd = ["python", "-m", "pytest"]
    if venv_path.exists():
        if sys.platform == "win32":
            python_path = venv_path / "Scripts" / "python.exe"
        else:
            python_path = venv_path / "bin" / "python"
        
        if python_path.exists():
            pytest_cmd = [str(python_path), "-m", "pytest"]
    
    print(f"\nExecutando pytest...")
    print(f"Comando: {' '.join(pytest_cmd)} tests/testE2E/test_e2e.py -v")
    print()
    
    result = subprocess.run(
        pytest_cmd + ["tests/testE2E/test_e2e.py", "-v"],
        cwd=str(project_root)
    )
    
    return result.returncode == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)


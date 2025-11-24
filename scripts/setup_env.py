#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, check=True):
    print(f"Executando: {command}")
    result = subprocess.run(command, shell=True, check=check)
    return result.returncode == 0


def setup_environment():
    project_root = Path(__file__).parent.parent
    venv_path = project_root / ".venv"
    
    print("=" * 60)
    print("Configurando ambiente de desenvolvimento")
    print("=" * 60)
    
    if not venv_path.exists():
        print("\n[1/3] Criando ambiente virtual...")
        run_command(f"python3 -m venv {venv_path}")
        print("✓ Ambiente virtual criado")
    else:
        print("\n[1/3] Ambiente virtual já existe")
    
    print("\n[2/3] Ativando ambiente virtual e instalando dependências...")
    pip_path = venv_path / "bin" / "pip"
    if sys.platform == "win32":
        pip_path = venv_path / "Scripts" / "pip.exe"
    
    if not pip_path.exists():
        print("✗ Erro: pip não encontrado no ambiente virtual")
        return False
    
    print(f"Instalando dependências usando {pip_path}...")
    run_command(f"{pip_path} install --upgrade pip")
    run_command(f"{pip_path} install -e .")
    
    print("\n[3/3] Instalando dependências de desenvolvimento...")
    run_command(f"{pip_path} install -e '.[dev]'")
    
    print("\n" + "=" * 60)
    print("✓ Ambiente configurado com sucesso!")
    print("=" * 60)
    print("\nPara ativar o ambiente virtual, execute:")
    if sys.platform == "win32":
        print(f"  {venv_path}\\Scripts\\activate")
    else:
        print(f"  source {venv_path}/bin/activate")
    print()
    
    return True


if __name__ == "__main__":
    success = setup_environment()
    sys.exit(0 if success else 1)


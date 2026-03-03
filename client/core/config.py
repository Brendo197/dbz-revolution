import os
import sys

def resource_path(relative_path: str) -> str:
    """
    Retorna o caminho correto tanto no Python normal
    quanto no executável gerado pelo PyInstaller.
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

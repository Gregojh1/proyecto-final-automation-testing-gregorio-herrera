import json
import os

def load_json_data(relative_path):
    """Carga y parsea un archivo JSON desde la raíz del proyecto."""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_path, relative_path)
    with open(full_path, "r", encoding="utf-8") as file:
        return json.load(file)
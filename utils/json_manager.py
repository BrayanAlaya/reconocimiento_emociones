import json

def load_json(filepath):
    """Carga y devuelve el contenido del archivo JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo {filepath} no existe.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: El archivo {filepath} no tiene un formato JSON válido.")
        return {}

def update_json_section(filepath, section, new_data):
    """Actualiza una sección específica en el archivo JSON sin afectar el resto del archivo."""
    data = load_json(filepath)

    if isinstance(data, dict):
        # Actualizar solo la sección específica
        data[section] = new_data
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except IOError:
            print(f"Error: No se pudo escribir en el archivo {filepath}.")
    else:
        print(f"Error: El archivo JSON {filepath} no tiene el formato esperado.")

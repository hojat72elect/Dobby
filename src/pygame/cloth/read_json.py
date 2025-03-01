import json

def read_json(path: str):
    try:
        with open(path, 'r') as f:
            data = f.read()
            return json.loads(data)
    except FileNotFoundError:
        print(f"The file was not found: {path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

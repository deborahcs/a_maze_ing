import sys
from typing import Any

def parse_coordinates(coord_str: str) -> tuple[int, int]:
    parts = coord_str.split(',')
    if len(parts) != 2:
        raise ValueError(f"Invalid coordinate format: '{coord_str}'. Expected 'x,y'.")
    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
        return (x, y)
    except ValueError:
        raise ValueError(f"Coordinates must be integers: '{coord_str}'.")

def read_config_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if not content.strip():
                raise ValueError("The configuration file is empty.")
            return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: '{file_path}'.")
    except Exception as e:
        raise Exception(f"Error reading file: {e}")

def create_raw_dict(content: str) -> dict[str, str]:
    raw_map = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            raise ValueError(f"Bad syntax in config: '{line}'. Expected KEY=VALUE.")

        key, value = line.split('=', 1)
        raw_map[key.strip().upper()] = value.strip()
    return raw_map

def validate_config(raw_map: dict[str, str]) -> dict[str, Any]:
    required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    for key in required:
        if key not in raw_map:
            raise KeyError(f"Missing mandatory key: {key}")

    config: dict[str, Any] = {}
    config['WIDTH'] = int(raw_map['WIDTH'])
    config['HEIGHT'] = int(raw_map['HEIGHT'])
    config['ENTRY'] = parse_coordinates(raw_map['ENTRY'])
    config['EXIT'] = parse_coordinates(raw_map['EXIT'])

    if config['ENTRY'] == config['EXIT']:
        raise ValueError("ENTRY and EXIT must be different points.")

    for key in ['ENTRY', 'EXIT']:
        x, y = config[key]
        if not (0 <= x < config['WIDTH'] and 0 <= y < config['HEIGHT']):
            raise ValueError(f"{key} coordinate ({x}, {y}) is outside maze bounds.")

    config['PERFECT'] = raw_map['PERFECT'].lower() == 'true'
    config['OUTPUT_FILE'] = raw_map['OUTPUT_FILE']
    
    # Suporte a SEED para reprodutibilidade [cite: 130]
    config['SEED'] = int(raw_map.get('SEED', 0))

    if config['WIDTH'] < 10 or config['HEIGHT'] < 10:
        print("Warning: Maze too small to draw '42' pattern.")
    
    return config

def get_maze_config(file_path: str) -> dict[str, Any]:
    content = read_config_file(file_path)
    raw_map = create_raw_dict(content)
    return validate_config(raw_map)
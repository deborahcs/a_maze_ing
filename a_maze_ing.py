import sys
import os
from parser import get_maze_config
from mazegen import MazeGenerator

def main() -> None:
    if len(sys.argv) != 2:
        print("Error: You must give an config file.")
        print("Use: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    
    config_path = sys.argv[1]

    if not os.path.exists(config_path):
        print(f"Error: The file '{config_path}' wasn't found.")
        sys.exit(1)

    print(f"Sucess: Reading configurations from {config_path}...")

    try:
        config = get_maze_config(config_path)
        print(f"Maze dimensions: {config['WIDTH']}x{config['HEIGHT']}")
        print(f"Start at: {config['ENTRY']} | Exit at: {config['EXIT']}")
        print(f"Perfect mode: {config['PERFECT']}")

        generator = MazeGenerator(config)
        grid = generator.generate()
        save_maze_to_file(config['OUTPUT_FILE'], grid)

    except Exception as error:
        print(f"Fatal Error: {error}")
        sys.exit(1)


def save_maze_to_file(filename, grid):
    try:
        with open(filename, 'w') as maze_file:
            for row in grid:
                line = "".join(f"{cell:X}" for cell in row)
                maze_file.write(line + "\n")
        print(f"Success: Maze saved to {filename}")
    
    except IOError as error:
        print(f"Fatal Error: Could not write to file {filename}: {error}")



if __name__ == "__main__":
    main()

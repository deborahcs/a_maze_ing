import sys
import os
from typing import NamedTuple
from parser import get_maze_config
from mazegen import MazeGenerator
from solver import solve_maze, path_to_string
from visualizer import draw_maze, clear_screen, display_menu

class ColorTheme(NamedTuple):
    label: str
    ansi_code: str

    COLORS = [
        ColorTheme("Blue", "\033[94m"),
        ColorTheme("Green", "\033[92m"),
        ColorTheme("Red", "\033[91m"),
        ColorTheme("Purple", "\033[95m") 
    ]

def save_maze_to_file(filename: str, grid: list[list[int]], entry: tuple[int, int],
                      exit: tuple[int, int], path: list[tuple[int, int]]) -> None:
    try:
        with open(filename, 'w', encoding="utf-8") as maze_file:
            for row in grid:
                maze_file.write("".join(f"{cell:X}" for cell in row) + "\n")
                maze_file.write("\n")
                maze_file.write(f"{entry[0]},{entry[1]}\n")
                maze_file.write(f"{exit[0]},{exit[1]}\n")
                maze_file.write(path_to_string(path) + "\n")
        print(f"Success: Maze saved to {filename}")
    except IOError as error:
        print(f"Fatal Error: Could not write to file: {error}") 

def main() -> None:
    config_path = sys.argv if len(sys.argv) > 1 else "config.txt"

    if not os.path.exists(config_path):
        print(f"Fatal Error: The file '{config_path}' wasn't found.")
        sys.exit(1)

    try:
        config = get_maze_config(config_path)
        generator = MazeGenerator(config)
        grid = generator.generate()
        solution = solve_maze(grid, config['ENTRY'], config['EXIT'])

        if not solution:
            print("Warning: Was not possible to find an solution for this Maze.")
        solution = []
        save_maze_to_file(config['OUTPUT_FILE'], grid, config['ENTRY'],
                          config['EXIT'], solution)
        show_path = True
        cor_idx = 0

        while True:
            clear_screen()
            actual_color = COLORS[cor_idx]
            print(f"Visual Configuration: {actual_color.label}")
            draw_maze(grid, solution, generator.pattern_42, show_path, actual_color.ansi_code)

        try:
            choice = display_menu()
        except (EOFError, KeyboardInterrupt):
            print("\nExecution ended by user. Ending process.")
            break

        if choice == "1":
            print("Generating new structure...")
            grid = generator.generate()
            solution = solve_maze(grid, config['ENTRY'], config['EXIT'])
            save_maze_to_file(config['OUTPUT_FILE'], grid, config['ENTRY'], config['EXIT'], solution)
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            cor_idx = (cor_idx + 1) % len(COLORS)
        elif choice == "4" or choice.lower() == 'q':
            print("Operation ended successfully. Ending program.")
            break

    except Exception as error:
        print(f"Fatal Error: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()

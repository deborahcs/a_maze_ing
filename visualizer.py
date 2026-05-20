import os
from typing import Optional


NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8

RESET: str = "\033[0m"
BG_BLACK: str = "\033[40m"
BG_PATH: str = "\033[46m"
BG_ENTRY: str = "\033[45m"
BG_EXIT: str = "\033[41m"
BG_42: str = "\033[43m"


def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def _cell_has_wall(cell: int, direction: int) -> bool:
    return bool(cell & direction)


def draw_maze(
    grid: list[list[int]],
    path: Optional[list[tuple[int, int]]],
    pattern_42: list[tuple[int, int]],
    show_path: bool,
    wall_color: str,
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
) -> None:
    height: int = len(grid)
    width: int = len(grid[0]) if height > 0 else 0

    path_set: set[tuple[int, int]] = set(path) if (path and show_path) else set()
    pattern_set: set[tuple[int, int]] = set(pattern_42)

    WALL_BLOCK: str = "  "
    OPEN_BLOCK: str = "  "

    def wall_str(is_wall: bool) -> str:
        if is_wall:
            return f"{wall_color}{BG_BLACK}{WALL_BLOCK}{RESET}"
        return WALL_BLOCK

    def cell_bg(x: int, y: int) -> str:
        if (x, y) == entry:
            return BG_ENTRY
        if (x, y) == exit_cell:
            return BG_EXIT
        if (x, y) in path_set:
            return BG_PATH
        if (x, y) in pattern_set:
            return BG_42
        return BG_BLACK

    lines: list[str] = []

    # Top border row
    top_row: str = ""
    for x in range(width):
        cell: int = grid[0][x]
        top_row += f"{wall_color}{BG_BLACK}{WALL_BLOCK}{RESET}"
        top_wall: bool = _cell_has_wall(cell, NORTH)
        top_row += f"{wall_color}{BG_BLACK}{WALL_BLOCK}{RESET}" if top_wall else \
                   f"{wall_color}{BG_BLACK}{WALL_BLOCK}{RESET}"
    top_row += f"{wall_color}{BG_BLACK}{WALL_BLOCK}{RESET}"
    lines.append(top_row)

    for y in range(height):
        row_a: str = ""
        row_b: str = ""

        for x in range(width):
            cell = grid[y][x]
            bg: str = cell_bg(x, y)

            left_wall: bool = _cell_has_wall(cell, WEST)
            right_wall: bool = _cell_has_wall(cell, EAST)
            bottom_wall: bool = _cell_has_wall(cell, SOUTH)

            if left_wall:
                row_a += f"{wall_color}{BG_BLACK}{WALL_BLOCK}{RESET}"
            else:
                row_a += f"{bg}{OPEN_BLOCK}{RESET}"

            row_a += f"{bg}{OPEN_BLOCK}{RESET}"

            if left_wall:
                row_b += f"{wall_color}{BG_BLACK}{WALL_BLOCK}{RESET}"
            else:
                row_b += f"{bg}{OPEN_BLOCK}{RESET}"

            if bottom_wall:
                row_b += f"{wall_color}{BG_BLACK}{WALL_BLOCK}{RESET}"
            else:
                row_b += f"{bg}{OPEN_BLOCK}{RESET}"

        last_cell: int = grid[y][width - 1]
        if _cell_has_wall(last_cell, EAST):
            row_a += f"{wall_color}{BG_BLACK}{WALL_BLOCK}{RESET}"
            row_b += f"{wall_color}{BG_BLACK}{WALL_BLOCK}{RESET}"
        else:
            row_a += f"{BG_BLACK}{OPEN_BLOCK}{RESET}"
            row_b += f"{BG_BLACK}{OPEN_BLOCK}{RESET}"

        lines.append(row_a)
        lines.append(row_b)

    print("\n".join(lines))
    print()


def display_menu() -> str:
    print("=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze wall colors")
    print("4. Quit")
    choice: str = input("Choice (1-4): ").strip()
    return choice

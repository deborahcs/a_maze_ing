from typing import Optional


MOVEMENTS: dict[str, tuple[int, int]] = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0)
}

OPEN_PATHS: dict[int, list[str]] = {
    0: ['N', 'E', 'S', 'W'], 1: ['E', 'S', 'W'], 2: ['N', 'S', 'W'], 3: ['S', 'W'],
    4: ['N', 'E', 'W'], 5: ['E', 'W'], 6: ['N', 'W'], 7: ['W'],
    8: ['N', 'E', 'S'], 9: ['E', 'S'], 10: ['N', 'S'], 11: ['S'],
    12: ['N', 'E'], 13: ['E'], 14: ['N'], 15: []
}


def reconstruct_path(parent_map: dict[tuple[int, int], Optional[tuple[int, int]]],
                     end_node: tuple[int, int]) -> list[tuple[int, int]]:
    path: list[tuple[int, int]] = []
    current: Optional[tuple[int, int]] = end_node

    while current is not None:
        path.append(current)
        current = parent_map[current]
    return path[::-1]


def solve_maze(grid: list[list[int]], start_node: tuple[int, int],
               end_node: tuple[int, int]) -> Optional[list[tuple[int, int]]]:
    queue: list[tuple[int, int]] = [start_node]
    visited: set[tuple[int, int]] = {start_node}
    parent_map: dict[tuple[int, int], Optional[tuple[int, int]]] = {start_node: None}
    
    height: int = len(grid)
    width: int = len(grid) if height > 0 else 0

    while queue:
        x, y = queue.pop(0)
        if (x, y) == end_node:
            return reconstruct_path(parent_map, end_node)
            
        cell_value: int = grid[y][x]
        for direction in OPEN_PATHS.get(cell_value, []):
            dx, dy = MOVEMENTS[direction]
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent_map[(nx, ny)] = (x, y)
                    queue.append((nx, ny))
    return None

def path_to_directions(path: list[tuple[int, int]]) -> str:
    if not path or len(path) < 2:
        return ""
    
    result: list[str] = []
    for i in range(len(path) - 1):
        cx, cy = path[i]
        nx, ny = path[i+1]
        if ny < cy: result.append("N")
        elif ny > cy: result.append("S")
        elif nx > cx: result.append("E")
        elif nx < cx: result.append("W")
    return "".join(result)
def load_maze(filename: str) -> list[list[int]]:
    grid = []
    with open(filename, 'r') as maze_file:
        for line in maze_file:
            row = [int(char, 16) for char in line.strip()]
            grid.append(row)
    return grid

import random


class MazeGenerator:
    def __init__(self, config: dict) -> None:
        self.width = config['WIDTH']
        self.height = config['HEIGHT']
        self.start_node = config['ENTRY']
        self.end_node = config['EXIT']
        self.seed = config.get('SEED', None)

        if self.seed is not None:
            random.seed(self.seed)

        self.grid = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]

        self.visited = [[False for _ in range(self.width)]
                        for _ in range(self.height)]

    def get_unvisited_neighbors(self, x: int, y: int) -> list:
        neighbors: list[tuple[int, int, int, int]] = []
        directions: list[tuple[int, int, int, int]] = [
            (0, -1, 1, 4),
            (1, 0, 2, 8),
            (0, 1, 4, 1),
            (-1, 0, 8, 2)
        ]

        for dx, dy, wall, opposite_wall in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.visited[ny][nx]:
                    neighbors.append((nx, ny, wall, opposite_wall))
        return neighbors

    def remove_wall(self, current_x, current_y,
                    next_x, next_y, wall, opposite_wall) -> None:
        self.grid[current_y][current_x] -= wall
        self.grid[next_y][next_x] -= opposite_wall

    def imperfect_lab(self, chance: float) -> None:
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if random.random() < chance:
                    if self.grid[y][x] >= 2:
                        self.grid[y][x] -= 2
                        self.grid[y][x + 1] -= 8

    def get_42_pattern(self) -> list[tuple[int, int]]:
        mid_x = self.width // 2
        mid_y = self.height // 2

        offsets = [
            (mid_x - 3, mid_y - 1), (mid_x - 3, mid_y), (mid_x - 3, mid_y + 1),
            (mid_x - 2, mid_y + 1), (mid_x - 1, mid_y - 1), (mid_x - 1, mid_y),
            (mid_x - 1, mid_y + 1), (mid_x - 1, mid_y + 2),
            (mid_x - 1, mid_y + 3), (mid_x + 1, mid_y - 1),
            (mid_x + 2, mid_y - 1), (mid_x + 3, mid_y - 1),
            (mid_x + 3, mid_y), (mid_x + 3, mid_y + 1),
            (mid_x + 2, mid_y + 1), (mid_x + 1, mid_y + 1),
            (mid_x + 1, mid_y + 2), (mid_x + 1, mid_y + 3),
            (mid_x + 2, mid_y + 3), (mid_x + 3, mid_y + 3)
        ]
        return offsets

    def apply_42_pattern(self) -> None:
        coordinates_42 = self.get_42_pattern()
        for x, y in coordinates_42:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = 15
                self.visited[y][x] = True

    def generate(self) -> list[list[int]]:
        if self.width < 10 or self.height < 10:
            print("Error: Maze size is to small to display the '42' pattern.")
        else:
            self.apply_42_pattern()

        start_x, start_y = self.start_node
        stack: list[tuple[int, int]] = [(start_x, start_y)]
        self.visited[start_y][start_x] = True

        while stack:
            current_x, current_y = stack[-1]
            neighbors = self.get_unvisited_neighbors(current_x, current_y)

            if neighbors:
                next_x, next_y, wall, opposite_wall = random.choice(neighbors)
                self.remove_wall(current_x, current_y,
                                 next_x, next_y, wall, opposite_wall)
                self.visited[next_y][next_x] = True
                stack.append((next_x, next_y))
            else:
                stack.pop()
        return self.grid

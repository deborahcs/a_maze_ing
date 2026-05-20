import random
from typing import Any, Optional


class MazeGenerator:
    def __init__(self, config: dict[str, Any]) -> None:
        self.width: int = config['WIDTH']
        self.height: int = config['HEIGHT']
        self.start_node: tuple[int, int] = config['ENTRY']
        self.end_node: tuple[int, int] = config['EXIT']
        self.seed: Optional[int] = config.get('SEED', None)
        self.perfect: bool = config.get('PERFECT', True)

        self.grid: list[list[int]] = []
        self.visited: list[list[bool]] = []
        self.pattern_42: list[tuple[int, int]] = []

    def _reset_state(self) -> None:
        self.grid = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]
        self.visited = [[False for _ in range(self.width)]
                        for _ in range(self.height)]

    def get_unvisited_neighbors(self, x: int,
                                y: int) -> list[tuple[int, int, int, int]]:
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

    def remove_wall(self, current_x: int, current_y: int,
                    next_x: int, next_y: int, wall: int,
                    opposite_wall: int) -> None:
        self.grid[current_y][current_x] &= ~wall
        self.grid[next_y][next_x] &= ~opposite_wall

    def imperfect_lab(self, chance: float) -> None:
        pattern_set: set[tuple[int, int]] = set(self.pattern_42)

        for y in range(self.height):
            for x in range(self.width - 1):
                if (x, y) in pattern_set or (x + 1, y) in pattern_set:
                    continue
                if random.random() < chance:
                    self.remove_wall(x, y, x + 1, y, 2, 8)

    def get_42_pattern(self) -> list[tuple[int, int]]:
        mid_x: int = self.width // 2
        mid_y: int = self.height // 2

        offsets: list[tuple[int, int]] = [
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
        return [
            (x, y) for x, y in offsets
            if 0 <= x < self.width and 0 <= y < self.height
        ]

    def apply_42_pattern(self) -> None:
        self.pattern_42 = self.get_42_pattern()
        for x, y in self.pattern_42:
            self.grid[y][x] = 15
            self.visited[y][x] = True

    def generate(self) -> list[list[int]]:
        if self.seed is not None:
            random.seed(self.seed)
        self._reset_state()

        if self.width < 10 or self.height < 10:
            print("Warning: Maze size is too small to display "
                  "the '42' pattern.")
            self.pattern_42 = []
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
                self.remove_wall(
                    current_x, current_y,
                    next_x, next_y,
                    wall, opposite_wall,
                )
                self.visited[next_y][next_x] = True
                stack.append((next_x, next_y))
            else:
                stack.pop()
        if not self.perfect:
            self.imperfect_lab(0.12)

        return self.grid

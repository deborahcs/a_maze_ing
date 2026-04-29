import random

class MazeGenerator:
    def __init__(self, config: dict):
        self.width = config['WIDTH']
        self.height = config['HEIGHT']
        self.start_node = config['ENTRY']
        self.end_node = ['EXIT']
        self.seed = config.get('SEED', None)

        if self.seed is not None:
            random.seed(self.seed)
        
        self.grid = [[15 for _ in range(self.width)] for _ in range(self.height)]

        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]

    def get_unvisited_neighbors(self, x: int, y: int) -> list:
        neighbors = []
        directions = [
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


    def remove_wall(self, current_x, current_y, next_x, next_y, wall, opposite_wall) -> None:
        self.grid[current_y][current_x] -= wall
        self.grid[next_y][next_x] -= opposite_wall


    def generate(self) -> list:
        start_x, start_y = self.start_node
        stack = [(start_x, start_y)]
        self.visited[start_y][start_x] = True

        while stack:
            current_x, current_y = stack[-1]
            neighbors = self.get_unvisited_neighbors(current_x, current_y)

            if neighbors:
                next_x, next_y, wall, opposite_wall = random.choice(neighbors)
                self.remove_wall(current_x, current_y, next_x, next_y, wall, opposite_wall)
                self.visited[next_y][next_x] = True
                stack.append((next_x, next_y))
            else:
                stack.pop()
        return self.grid

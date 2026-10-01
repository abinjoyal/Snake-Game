import heapq
from game.snake import Snake
from settings import GRID_WIDTH, GRID_HEIGHT, MAZE_OBSTACLES

class AISnake(Snake):
    """
    AI-controlled Snake opponent utilizing A* Pathfinding and safety heuristics
    to intelligently hunt food while avoiding walls, self-collision, and player 1.
    """
    def __init__(self, start_x=22, start_y=12, default_dir=(-1, 0), skin_key="blue"):
        super().__init__(start_x, start_y, default_dir, skin_key)

    def update_ai_direction(self, target_pos, obstacle_positions):
        """
        Calculates optimal next direction towards target_pos using A* pathfinding.
        Falls back to safest adjacent tile if direct path is trapped.
        """
        head = self.body[0]
        obstacles = set(obstacle_positions)
        obstacles.update(self.body)  # Avoid own body

        # A* Search to target food
        path = self._a_star_search(head, target_pos, obstacles)

        if path and len(path) > 1:
            next_tile = path[1]
            dx = next_tile[0] - head[0]
            dy = next_tile[1] - head[1]
            self.set_direction((dx, dy))
        else:
            # Fallback Safety Move: Pick adjacent tile with maximum free neighbors
            best_dir = None
            max_freedom = -1
            possible_dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]

            for d in possible_dirs:
                curr_dx, curr_dy = self.direction
                if d[0] == -curr_dx and d[1] == -curr_dy:
                    continue  # Do not reverse into self

                candidate_x = head[0] + d[0]
                candidate_y = head[1] + d[1]

                if 0 <= candidate_x < GRID_WIDTH and 0 <= candidate_y < GRID_HEIGHT:
                    if (candidate_x, candidate_y) not in obstacles:
                        # Count free neighbors of candidate tile
                        freedom = sum(
                            1 for nx, ny in [(candidate_x+1, candidate_y), (candidate_x-1, candidate_y),
                                             (candidate_x, candidate_y+1), (candidate_x, candidate_y-1)]
                            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in obstacles
                        )
                        if freedom > max_freedom:
                            max_freedom = freedom
                            best_dir = d

            if best_dir:
                self.set_direction(best_dir)

    def _a_star_search(self, start, goal, obstacles):
        """Standard A* pathfinding algorithm returning path tile list."""
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT:
                    if neighbor in obstacles and neighbor != goal:
                        continue

                    tentative_g = g_score[current] + 1
                    if tentative_g < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

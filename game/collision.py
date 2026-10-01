from settings import GRID_WIDTH, GRID_HEIGHT, MAZE_OBSTACLES

def check_wall_collision(head_position, map_mode="CLASSIC"):
    """
    Checks if snake head hit boundary walls.
    Ignored in PORTAL mode where wrap-around is active.
    """
    if map_mode == "PORTAL":
        return False
    x, y = head_position
    return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT

def check_obstacle_collision(head_position, map_mode="CLASSIC", custom_obstacles=None):
    """
    Checks if snake head hit any inner brick obstacles in OBSTACLES, CAMPAIGN, or CUSTOM maze modes.
    """
    if map_mode == "OBSTACLES":
        return head_position in MAZE_OBSTACLES
    elif map_mode == "CUSTOM" and custom_obstacles is not None:
        return head_position in custom_obstacles
    elif map_mode == "CAMPAIGN" and custom_obstacles is not None:
        return head_position in custom_obstacles
    return False

def check_self_collision(head_position, snake_body):
    """
    Checks if snake head position matches any body segment (excluding head).
    """
    return head_position in snake_body[1:]

def check_food_collision(head_position, food_position):
    """
    Checks if snake head has eaten the food tile.
    """
    return head_position == food_position

def check_snake_vs_snake_collision(head1, body2):
    """
    In 2-Player mode, checks if Head of Snake 1 collides with any part of Snake 2's body.
    """
    return head1 in body2

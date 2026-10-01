import random
import math
import pygame
from settings import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, FOOD_TYPES,
    MAZE_OBSTACLES
)

class Food:
    """
    Food item object supporting multiple power-up variants (Apple, Golden Star,
    Speed Lightning, Slow Turtle, Shrink Berry) with pulse animations and despawn timers.
    """
    def __init__(self):
        self.position = (0, 0)
        self.type_key = "NORMAL"
        self.type_info = FOOD_TYPES["NORMAL"]
        self.pulse_timer = 0.0
        self.lifetime = None  # None for normal food, int for timed food

    def respawn(self, occupied_positions, active_map_mode="CLASSIC"):
        """
        Spawns a new food item at a random grid tile that is not occupied by
        any snake body or maze obstacles.
        """
        all_tiles = set((x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT))
        occupied_tiles = set(occupied_positions)

        # Include maze obstacles if in OBSTACLES mode
        if active_map_mode == "OBSTACLES":
            occupied_tiles.update(MAZE_OBSTACLES)

        available_tiles = list(all_tiles - occupied_tiles)

        if available_tiles:
            self.position = random.choice(available_tiles)
        else:
            self.position = (0, 0)

        # Randomly choose food type based on defined spawn chances
        rand_val = random.random()
        cumulative = 0.0
        chosen_type = "NORMAL"

        for key, data in FOOD_TYPES.items():
            cumulative += data["chance"]
            if rand_val <= cumulative:
                chosen_type = key
                break

        self.type_key = chosen_type
        self.type_info = FOOD_TYPES[chosen_type]
        self.lifetime = self.type_info.get("lifetime", None)

    def update(self):
        """
        Updates pulse animation timer and despawn countdown.
        Returns True if food expired and needs despawning, False otherwise.
        """
        self.pulse_timer += 0.08
        if self.lifetime is not None:
            self.lifetime -= 1
            if self.lifetime <= 0:
                return True
        return False

    def draw(self, surface):
        """Renders food item with variant-specific colors and visual indicators."""
        gx, gy = self.position
        pixel_x = gx * GRID_SIZE
        pixel_y = gy * GRID_SIZE
        center_x = pixel_x + GRID_SIZE // 2
        center_y = pixel_y + GRID_SIZE // 2

        scale = 0.5 + 0.1 * math.sin(self.pulse_timer)
        radius = int((GRID_SIZE // 2 - 2) * scale * 1.8)
        color = self.type_info["color"]

        # Outer glowing halo
        glow_surface = pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)
        glow_alpha = 90 if self.type_key == "GOLDEN" else 50
        
        # Flash glow if timed food is about to expire (< 90 frames)
        if self.lifetime is not None and self.lifetime < 90 and (self.lifetime // 10) % 2 == 0:
            glow_alpha = 10

        pygame.draw.circle(glow_surface, (*color, glow_alpha), (GRID_SIZE, GRID_SIZE), radius + 5)
        surface.blit(glow_surface, (center_x - GRID_SIZE, center_y - GRID_SIZE))

        # Render Main Icon Shape
        if self.type_key == "GOLDEN":
            # Star shape or multi-circle star
            pygame.draw.circle(surface, color, (center_x, center_y), radius)
            pygame.draw.circle(surface, (255, 255, 255), (center_x, center_y), radius // 2)
        elif self.type_key == "SPEED_BOOST":
            # Diamond shape
            pts = [
                (center_x, center_y - radius),
                (center_x + radius, center_y),
                (center_x, center_y + radius),
                (center_x - radius, center_y)
            ]
            pygame.draw.polygon(surface, color, pts)
        elif self.type_key == "SLOW_MO":
            # Rounded box
            rect = pygame.Rect(center_x - radius, center_y - radius, radius * 2, radius * 2)
            pygame.draw.rect(surface, color, rect, border_radius=5)
        elif self.type_key == "MAGNET":
            # Horseshoe Magnet Shape
            pygame.draw.circle(surface, color, (center_x, center_y), radius)
            pygame.draw.circle(surface, (255, 255, 255), (center_x, center_y), radius // 2, width=2)
        elif self.type_key == "SHIELD":
            # Shield Bubble Shield Circle
            pygame.draw.circle(surface, color, (center_x, center_y), radius)
            pygame.draw.circle(surface, (255, 255, 255), (center_x, center_y), radius - 3, width=2)
        elif self.type_key == "SHRINK":
            # Hexagon / Purple Berry
            pygame.draw.circle(surface, color, (center_x, center_y), radius)
            pygame.draw.circle(surface, (233, 213, 255), (center_x - radius // 3, center_y - radius // 3), 2)
        else:
            # Standard Apple
            pygame.draw.circle(surface, color, (center_x, center_y), radius)
            pygame.draw.circle(surface, (254, 202, 202), (center_x - radius // 3, center_y - radius // 3), 2)
            # Leaf
            pygame.draw.circle(surface, (52, 211, 153), (center_x + 1, center_y - radius - 1), 2)

import colorsys
import pygame
from settings import GRID_SIZE, SKINS

class Snake:
    """
    Snake game object handling body coordinates, direction changes,
    growth, shrink, reset, and skin-based rendering.
    """
    def __init__(self, start_x=10, start_y=10, default_dir=(1, 0), skin_key="classic"):
        self.start_x = start_x
        self.start_y = start_y
        self.default_dir = default_dir
        self.default_skin = skin_key
        self.reset()

    def reset(self):
        """Resets snake to initial position and default direction."""
        dx, dy = self.default_dir
        self.body = [
            (self.start_x, self.start_y),
            (self.start_x - dx, self.start_y - dy),
            (self.start_x - dx * 2, self.start_y - dy * 2)
        ]
        self.direction = self.default_dir
        self.next_direction = self.default_dir
        self.growing = False
        self.shrink_count = 0
        self.skin_key = self.default_skin
        self.shield_active = False

    def activate_shield(self):
        """Activates defensive energy shield bubble."""
        self.shield_active = True

    def pop_shield(self):
        """Pops shield bubble upon absorbing fatal hit."""
        was_active = self.shield_active
        self.shield_active = False
        return was_active

    def set_direction(self, new_dir):
        """
        Updates target direction if it is not directly opposite
        to current or queued direction.
        """
        curr_dx, curr_dy = self.direction
        new_dx, new_dy = new_dir

        if (new_dx != -curr_dx or new_dx == 0) and (new_dy != -curr_dy or new_dy == 0):
            self.next_direction = new_dir

    def update(self, wrap_portal=False, grid_width=32, grid_height=24):
        """
        Advances the snake by one grid tile in the current direction.
        Supports optional portal wrap-around grid math.
        """
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction

        new_head_x = head_x + dx
        new_head_y = head_y + dy

        # Portal Wrap-Around Mode Math
        if wrap_portal:
            new_head_x = new_head_x % grid_width
            new_head_y = new_head_y % grid_height

        new_head = (new_head_x, new_head_y)
        self.body.insert(0, new_head)

        if self.growing:
            self.growing = False
        elif self.shrink_count > 0:
            # Shrink: remove extra segment if snake length > 3
            if len(self.body) > 3:
                self.body.pop()
            if len(self.body) > 3:
                self.body.pop()
            self.shrink_count = 0
        else:
            self.body.pop()

        return new_head

    def grow(self, count=1):
        """Signals the snake to grow on update step."""
        self.growing = True

    def shrink(self, amount=2):
        """Signals the snake to shrink its body length."""
        self.shrink_count = amount

    def get_head_position(self):
        """Returns the grid coordinate tuple of the snake's head."""
        return self.body[0]

    def set_skin(self, skin_key):
        """Sets active skin for rendering."""
        if skin_key in SKINS:
            self.skin_key = skin_key

    def draw(self, surface, tick_count=0):
        """
        Renders the snake body segments and head with custom skin styling.
        """
        skin_data = SKINS.get(self.skin_key, SKINS["classic"])
        total_segments = len(self.body)

        for i, (gx, gy) in enumerate(self.body):
            pixel_x = gx * GRID_SIZE
            pixel_y = gy * GRID_SIZE
            rect = pygame.Rect(pixel_x + 1, pixel_y + 1, GRID_SIZE - 2, GRID_SIZE - 2)

            if i == 0:
                # Head
                color = skin_data["head"]
                pygame.draw.rect(surface, color, rect, border_radius=6)
                self._draw_eyes(surface, rect, skin_data.get("eye_color", (255, 255, 255)))

                # Render Shield Bubble Aura
                if self.shield_active:
                    cx, cy = rect.center
                    shield_surf = pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)
                    pygame.draw.circle(shield_surf, (56, 189, 248, 120), (GRID_SIZE, GRID_SIZE), GRID_SIZE - 2)
                    pygame.draw.circle(shield_surf, (56, 189, 248, 240), (GRID_SIZE, GRID_SIZE), GRID_SIZE - 2, width=2)
                    surface.blit(shield_surf, (cx - GRID_SIZE, cy - GRID_SIZE))
            else:
                # Body Segment Styling
                if self.skin_key == "rainbow":
                    hue = (tick_count * 0.02 + i * 0.08) % 1.0
                    r, g, b = colorsys.hsv_to_rgb(hue, 0.9, 0.95)
                    color = (int(r * 255), int(g * 255), int(b * 255))
                else:
                    t = i / float(total_segments)
                    start_c = skin_data["body_start"]
                    end_c = skin_data["body_end"]
                    color = (
                        int(start_c[0] + (end_c[0] - start_c[0]) * t),
                        int(start_c[1] + (end_c[1] - start_c[1]) * t),
                        int(start_c[2] + (end_c[2] - start_c[2]) * t)
                    )

                pygame.draw.rect(surface, color, rect, border_radius=4)

    def _draw_eyes(self, surface, head_rect, eye_color):
        """Draws two small eyes facing direction of movement."""
        dx, dy = self.direction
        cx, cy = head_rect.center
        eye_radius = 2.5
        pupil_radius = 1.2
        offset = 5

        if dx == 1:    # Right
            eye1_pos = (cx + offset, cy - offset)
            eye2_pos = (cx + offset, cy + offset)
        elif dx == -1: # Left
            eye1_pos = (cx - offset, cy - offset)
            eye2_pos = (cx - offset, cy + offset)
        elif dy == -1: # Up
            eye1_pos = (cx - offset, cy - offset)
            eye2_pos = (cx + offset, cy - offset)
        else:          # Down
            eye1_pos = (cx - offset, cy + offset)
            eye2_pos = (cx + offset, cy + offset)

        pygame.draw.circle(surface, eye_color, eye1_pos, eye_radius)
        pygame.draw.circle(surface, eye_color, eye2_pos, eye_radius)
        pygame.draw.circle(surface, (10, 15, 30), eye1_pos, pupil_radius)
        pygame.draw.circle(surface, (10, 15, 30), eye2_pos, pupil_radius)

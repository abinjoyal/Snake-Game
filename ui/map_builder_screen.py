import os
import json
import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT,
    BG_DARK, BG_COLOR, GRID_LINE_COLOR, PANEL_BG, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT_GREEN, ACCENT_RED, CUSTOM_MAP_FILE
)
from ui.components import Button

class MapBuilderScreen:
    """
    Interactive tile grid editor screen allowing players to paint/erase
    custom brick obstacle maps and save them to data/custom_map.json.
    """
    def __init__(self, game_state_manager):
        self.gsm = game_state_manager
        self.custom_obstacles = set()
        self.load_custom_map()

        btn_font = pygame.font.SysFont("Segoe UI", 14, bold=True)
        btn_y = WINDOW_HEIGHT - 65

        self.save_button = Button(
            (WINDOW_WIDTH // 2 - 210, btn_y, 130, 45),
            "SAVE MAP",
            lambda: self._on_save_clicked(),
            btn_font,
            bg_color=ACCENT_GREEN,
            hover_color=(52, 211, 153),
            text_color=TEXT_PRIMARY
        )
        self.clear_button = Button(
            (WINDOW_WIDTH // 2 - 65, btn_y, 130, 45),
            "CLEAR ALL",
            lambda: self.custom_obstacles.clear(),
            btn_font,
            bg_color=ACCENT_RED,
            hover_color=(248, 113, 113),
            text_color=TEXT_PRIMARY
        )
        self.back_button = Button(
            (WINDOW_WIDTH // 2 + 80, btn_y, 130, 45),
            "BACK TO MENU",
            lambda: self._on_back_clicked(),
            btn_font,
            bg_color=(51, 65, 85),
            hover_color=(71, 85, 105),
            text_color=TEXT_PRIMARY
        )

    def _on_save_clicked(self):
        self.save_custom_map()
        from game.game_state import State
        self.gsm.set_state(State.MENU)

    def _on_back_clicked(self):
        from game.game_state import State
        self.gsm.set_state(State.MENU)

    def load_custom_map(self):
        """Loads custom obstacle coordinates from JSON file."""
        if os.path.exists(CUSTOM_MAP_FILE):
            try:
                with open(CUSTOM_MAP_FILE, "r") as f:
                    data = json.load(f)
                    self.custom_obstacles = set(tuple(p) for p in data.get("obstacles", []))
            except Exception as e:
                print(f"[MapBuilderScreen] Error loading custom map: {e}")

    def save_custom_map(self):
        """Saves custom obstacle coordinates to JSON file."""
        try:
            data = {"obstacles": [list(p) for p in self.custom_obstacles]}
            with open(CUSTOM_MAP_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[MapBuilderScreen] Error saving custom map: {e}")

    def handle_event(self, event):
        self.save_button.handle_event(event, self.gsm.sound_manager)
        self.clear_button.handle_event(event, self.gsm.sound_manager)
        self.back_button.handle_event(event, self.gsm.sound_manager)

        # Mouse Click/Drag on Grid to Paint Wall Bricks
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            if pygame.mouse.get_pressed()[0]:  # Left Click / Drag
                mx, my = event.pos
                if 0 <= mx < WINDOW_WIDTH and 0 <= my < WINDOW_HEIGHT - 80:
                    gx = mx // GRID_SIZE
                    gy = my // GRID_SIZE
                    # Prevent placing obstacles in default starting positions of P1 / P2
                    if (gx, gy) not in [(10, 12), (9, 12), (8, 12), (22, 12), (23, 12), (24, 12)]:
                        self.custom_obstacles.add((gx, gy))
            elif pygame.mouse.get_pressed()[2]: # Right Click to erase
                mx, my = event.pos
                if 0 <= mx < WINDOW_WIDTH and 0 <= my < WINDOW_HEIGHT - 80:
                    gx = mx // GRID_SIZE
                    gy = my // GRID_SIZE
                    self.custom_obstacles.discard((gx, gy))

    def draw(self, surface):
        surface.fill(BG_COLOR)

        # Draw Grid Lines
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(surface, GRID_LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT - 80))
        for y in range(0, WINDOW_HEIGHT - 80, GRID_SIZE):
            pygame.draw.line(surface, GRID_LINE_COLOR, (0, y), (WINDOW_WIDTH, y))

        # Render Placed Custom Obstacle Bricks
        for gx, gy in self.custom_obstacles:
            px = gx * GRID_SIZE
            py = gy * GRID_SIZE
            rect = pygame.Rect(px + 1, py + 1, GRID_SIZE - 2, GRID_SIZE - 2)
            pygame.draw.rect(surface, (148, 163, 184), rect, border_radius=4)
            pygame.draw.rect(surface, (71, 85, 105), rect, width=2, border_radius=4)

        # Bottom Control Panel Background
        panel_rect = pygame.Rect(0, WINDOW_HEIGHT - 80, WINDOW_WIDTH, 80)
        pygame.draw.rect(surface, PANEL_BG, panel_rect)
        pygame.draw.line(surface, (51, 65, 85), (0, WINDOW_HEIGHT - 80), (WINDOW_WIDTH, WINDOW_HEIGHT - 80), 2)

        # Header Instructions
        font = pygame.font.SysFont("Segoe UI", 14)
        info_str = f"CUSTOM MAP BUILDER: Left Click to Paint Brick Wall, Right Click to Erase ({len(self.custom_obstacles)} Bricks)"
        info_lbl = font.render(info_str, True, TEXT_MUTED)
        surface.blit(info_lbl, (15, WINDOW_HEIGHT - 75))

        self.save_button.draw(surface)
        self.clear_button.draw(surface)
        self.back_button.draw(surface)

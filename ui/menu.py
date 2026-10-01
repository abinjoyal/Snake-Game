import math
import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, GRID_LINE_COLOR,
    GRID_SIZE, TEXT_PRIMARY, TEXT_MUTED, ACCENT_GREEN, ACCENT_GOLD,
    ACCENT_BLUE, ACCENT_PURPLE, ACCENT_RED, MAP_MODES, PANEL_BG
)
from ui.components import Button, draw_text, draw_text_glow
from game.game_state import State

class MainMenuScreen:
    """
    Main Menu user interface featuring glowing neon title graphics,
    mode selectors (1P/2P/VS_AI, Map Mode), high score badge, and navigation buttons.
    """
    def __init__(self, game_state, title_font, font, small_font, quit_callback):
        self.game_state = game_state
        self.title_font = title_font
        self.font = font
        self.small_font = small_font
        self.quit_callback = quit_callback
        
        self.anim_timer = 0.0

        btn_w, btn_h = 240, 44
        center_x = WINDOW_WIDTH // 2 - btn_w // 2
        start_y = 230
        spacing = 50

        # Top Control Bar Cards for Mode & Map Selectors
        self.btn_mode = Button((WINDOW_WIDTH // 2 - 250, 150, 235, 40),
                               self._get_mode_label(), self._toggle_mode, small_font,
                               hover_color=ACCENT_BLUE)
        self.btn_map = Button((WINDOW_WIDTH // 2 + 15, 150, 235, 40),
                              self._get_map_label(), self._toggle_map, small_font,
                              hover_color=ACCENT_PURPLE)

        # Primary Navigation Buttons
        self.buttons = [
            Button((center_x, start_y, btn_w, btn_h), "PLAY GAME",
                   lambda: self.game_state.start_new_game(), font,
                   hover_color=ACCENT_GREEN),
            Button((center_x, start_y + spacing, btn_w, btn_h), "ACHIEVEMENTS",
                   lambda: self.game_state.set_state(State.ACHIEVEMENTS), font,
                   hover_color=ACCENT_GOLD),
            Button((center_x, start_y + spacing * 2, btn_w, btn_h), "MAP BUILDER",
                   lambda: self.game_state.set_state(State.MAP_BUILDER), font,
                   hover_color=ACCENT_BLUE),
            Button((center_x, start_y + spacing * 3, btn_w, btn_h), "SNAKE SKINS",
                   lambda: self.game_state.set_state(State.SKINS), font,
                   hover_color=ACCENT_PURPLE),
            Button((center_x, start_y + spacing * 4, btn_w, btn_h), "LEADERBOARD",
                   lambda: self.game_state.set_state(State.LEADERBOARD), font,
                   hover_color=ACCENT_GOLD),
            Button((center_x, start_y + spacing * 5, btn_w, btn_h), "SETTINGS",
                   lambda: self.game_state.set_state(State.SETTINGS), font,
                   hover_color=ACCENT_BLUE),
            Button((center_x, start_y + spacing * 6, btn_w, btn_h), "EXIT GAME",
                   self.quit_callback, font,
                   hover_color=(220, 38, 38))
        ]

    def _get_mode_label(self):
        modes = {"1P": "1-PLAYER SOLO", "2P": "2-PLAYER VERSUS", "VS_AI": "VS AI BOT"}
        return f"MODE: {modes.get(self.game_state.game_mode, '1P')}"

    def _get_map_label(self):
        return f"MAP: {MAP_MODES.get(self.game_state.map_mode, 'Classic')}"

    def _toggle_mode(self):
        modes = ["1P", "2P", "VS_AI"]
        curr_idx = modes.index(self.game_state.game_mode) if self.game_state.game_mode in modes else 0
        next_idx = (curr_idx + 1) % len(modes)
        self.game_state.game_mode = modes[next_idx]
        self.btn_mode.text = self._get_mode_label()

    def _toggle_map(self):
        modes = list(MAP_MODES.keys())
        curr_idx = modes.index(self.game_state.map_mode) if self.game_state.map_mode in modes else 0
        next_idx = (curr_idx + 1) % len(modes)
        self.game_state.map_mode = modes[next_idx]
        self.btn_map.text = self._get_map_label()

    def handle_event(self, event):
        """Dispatches event to menu buttons and mode selectors."""
        self.btn_mode.handle_event(event, self.game_state.sound_manager)
        self.btn_map.handle_event(event, self.game_state.sound_manager)
        
        for btn in self.buttons:
            btn.handle_event(event, self.game_state.sound_manager)

    def update(self):
        """Updates background animation timer."""
        self.anim_timer += 0.05

    def draw(self, surface):
        """Renders main menu screen graphics."""
        surface.fill(BG_COLOR)
        self._draw_grid_background(surface)
        self._draw_decorative_snake(surface)

        # Title Neon Glow
        title_y = 65 + int(math.sin(self.anim_timer) * 3)
        draw_text_glow(surface, "SNAKE GAME", self.title_font, ACCENT_GREEN, (4, 120, 87), (WINDOW_WIDTH // 2, title_y))

        # Top Control Container Card for Mode Selectors
        control_card = pygame.Rect(WINDOW_WIDTH // 2 - 270, 138, 540, 62)
        pygame.draw.rect(surface, PANEL_BG, control_card, border_radius=12)
        pygame.draw.rect(surface, (50, 65, 85), control_card, width=1, border_radius=12)

        self.btn_mode.draw(surface)
        self.btn_map.draw(surface)

        # High Score Badge Pill
        high_score = self.game_state.leaderboard_manager.get_high_score()
        draw_text(surface, f"BEST RECORD: {high_score}", self.small_font, ACCENT_GOLD, (WINDOW_WIDTH // 2, 212))

        # Render Navigation Buttons
        for btn in self.buttons:
            btn.draw(surface)

    def _draw_grid_background(self, surface):
        """Draws clean dark background grid lines."""
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(surface, GRID_LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, GRID_LINE_COLOR, (0, y), (WINDOW_WIDTH, y))

    def _draw_decorative_snake(self, surface):
        """Draws subtle sine-wave animated snake background graphic."""
        for i in range(14):
            x = (int(self.anim_timer * 60) + i * 20) % (WINDOW_WIDTH + 100) - 50
            y = 575 + int(math.sin(self.anim_timer + i * 0.4) * 8)
            color = (16, 185, 129, 90) if i == 0 else (52, 211, 153, 50)
            
            s = pygame.Surface((16, 16), pygame.SRCALPHA)
            pygame.draw.rect(s, color, (0, 0, 16, 16), border_radius=4)
            surface.blit(s, (x, y))

import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, PANEL_BG,
    TEXT_PRIMARY, TEXT_MUTED, ACCENT_GREEN, ACCENT_RED, ACCENT_BLUE
)
from ui.components import Button, draw_text, draw_text_glow
from game.game_state import State

class SettingsScreen:
    """
    Settings screen offering sound toggles, BGM toggles, game speed selection,
    map mode choice, and a controls reference guide.
    """
    def __init__(self, game_state, title_font, font, small_font):
        self.game_state = game_state
        self.title_font = title_font
        self.font = font
        self.small_font = small_font

        cx = WINDOW_WIDTH // 2
        btn_w, btn_h = 180, 40

        # Sound & BGM Toggle Buttons
        self.btn_sound = Button(
            (cx - 195, 140, btn_w, btn_h),
            self._get_sound_label(),
            self._toggle_sound,
            font
        )
        self.btn_bgm = Button(
            (cx + 15, 140, btn_w, btn_h),
            self._get_bgm_label(),
            self._toggle_bgm,
            font
        )

        # Map Mode Selectors
        self.map_buttons = [
            ("CLASSIC", Button((cx - 165, 230, 105, 36), "Classic", lambda: self._set_map("CLASSIC"), small_font)),
            ("PORTAL", Button((cx - 50, 230, 100, 36), "Portal", lambda: self._set_map("PORTAL"), small_font)),
            ("OBSTACLES", Button((cx + 60, 230, 105, 36), "Maze", lambda: self._set_map("OBSTACLES"), small_font))
        ]

        # Speed Options
        self.speed_buttons = [
            ("Slow", 5, Button((cx - 200, 310, 90, 36), "Slow", lambda: self._set_speed(5), small_font)),
            ("Normal", 8, Button((cx - 95, 310, 90, 36), "Normal", lambda: self._set_speed(8), small_font)),
            ("Fast", 12, Button((cx + 10, 310, 90, 36), "Fast", lambda: self._set_speed(12), small_font)),
            ("Insane", 16, Button((cx + 115, 310, 90, 36), "Insane", lambda: self._set_speed(16), small_font))
        ]

        # Back Button
        self.btn_back = Button(
            (cx - 100, 535, 200, 44),
            "BACK TO MENU",
            lambda: self.game_state.set_state(State.MENU),
            font
        )

    def _get_sound_label(self):
        enabled = self.game_state.sound_manager.enabled
        return f"SFX: {'ON' if enabled else 'OFF'}"

    def _get_bgm_label(self):
        enabled = self.game_state.sound_manager.bgm_enabled
        return f"MUSIC: {'ON' if enabled else 'OFF'}"

    def _toggle_sound(self):
        self.game_state.sound_manager.toggle_sound()
        self.btn_sound.text = self._get_sound_label()

    def _toggle_bgm(self):
        self.game_state.sound_manager.toggle_bgm()
        self.btn_bgm.text = self._get_bgm_label()

    def _set_map(self, map_mode):
        self.game_state.map_mode = map_mode

    def _set_speed(self, speed):
        self.game_state.game_speed = speed

    def handle_event(self, event):
        """Dispatches click events to setting toggles and back button."""
        self.btn_sound.handle_event(event, self.game_state.sound_manager)
        self.btn_bgm.handle_event(event, self.game_state.sound_manager)
        
        for key, btn in self.map_buttons:
            btn.handle_event(event, self.game_state.sound_manager)

        for name, spd, btn in self.speed_buttons:
            btn.handle_event(event, self.game_state.sound_manager)
            
        self.btn_back.handle_event(event, self.game_state.sound_manager)

    def draw(self, surface):
        """Renders settings screen components and controls guide."""
        surface.fill(BG_COLOR)

        # Header Title
        draw_text_glow(surface, "SETTINGS", self.title_font, ACCENT_BLUE, (3, 105, 161), (WINDOW_WIDTH // 2, 55))
        draw_text(surface, "Customize Audio, Map Layout, & Speed", self.small_font, TEXT_MUTED, (WINDOW_WIDTH // 2, 90))

        cx = WINDOW_WIDTH // 2

        # Sound Section
        draw_text(surface, "AUDIO & MUSIC SETTINGS", self.small_font, TEXT_MUTED, (cx, 120))
        self.btn_sound.bg_color = ACCENT_GREEN if self.game_state.sound_manager.enabled else (60, 70, 85)
        self.btn_bgm.bg_color = ACCENT_GREEN if self.game_state.sound_manager.bgm_enabled else (60, 70, 85)

        self.btn_sound.draw(surface)
        self.btn_bgm.draw(surface)

        # Map Mode Section
        draw_text(surface, "MAP BOUNDARY MODE", self.small_font, TEXT_MUTED, (cx, 205))
        for key, btn in self.map_buttons:
            btn.border_color = ACCENT_GREEN if self.game_state.map_mode == key else None
            btn.draw(surface)

        # Speed Section
        draw_text(surface, "GAME SPEED / DIFFICULTY", self.small_font, TEXT_MUTED, (cx, 285))
        for name, spd, btn in self.speed_buttons:
            btn.border_color = ACCENT_GREEN if self.game_state.game_speed == spd else None
            btn.draw(surface)

        # Controls Guide Card
        card_w, card_h = 520, 140
        card_rect = pygame.Rect(cx - card_w // 2, 370, card_w, card_h)
        pygame.draw.rect(surface, PANEL_BG, card_rect, border_radius=12)
        pygame.draw.rect(surface, (50, 65, 85), card_rect, width=1, border_radius=12)

        draw_text(surface, "CONTROLS REFERENCE", self.font, TEXT_PRIMARY, (cx, card_rect.y + 22))
        draw_text(surface, "• P1 Movement: W / A / S / D  |  P2 Movement: Arrow Keys", self.small_font, TEXT_MUTED, (cx, card_rect.y + 55))
        draw_text(surface, "• Pause Game: Press 'P' or ESC Key", self.small_font, TEXT_MUTED, (cx, card_rect.y + 85))
        draw_text(surface, "• Quick Restart: Press 'R' Key", self.small_font, TEXT_MUTED, (cx, card_rect.y + 112))

        # Back Button
        self.btn_back.draw(surface)

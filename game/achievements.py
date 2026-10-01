import os
import json
import pygame
from settings import ACHIEVEMENTS_FILE, WINDOW_WIDTH, ACCENT_GOLD, BG_DARK, TEXT_PRIMARY, PANEL_BG

ACHIEVEMENT_LIST = {
    "FIRST_EAT": {
        "title": "First Bite",
        "desc": "Eat your first apple in the game.",
        "icon": "🍎"
    },
    "COMBO_3": {
        "title": "Combo Streak",
        "desc": "Reach a 3x score multiplier.",
        "icon": "🔥"
    },
    "COMBO_5": {
        "title": "Combo Master",
        "desc": "Reach the maximum 5x score multiplier.",
        "icon": "⚡"
    },
    "SHIELD_SAVE": {
        "title": "Life Saver",
        "desc": "Absorb a fatal collision with a Shield Bubble.",
        "icon": "🛡️"
    },
    "MAGNET_MASTER": {
        "title": "Food Magnet",
        "desc": "Collect and activate a Food Magnet power-up.",
        "icon": "🧲"
    },
    "SCORE_100": {
        "title": "Centurion",
        "desc": "Score 100+ points in single-player mode.",
        "icon": "🏆"
    },
    "SCORE_300": {
        "title": "Snake Royalty",
        "desc": "Score 300+ points in single-player mode.",
        "icon": "👑"
    },
    "BOT_BUSTER": {
        "title": "Bot Buster",
        "desc": "Defeat the AI Bot snake in Player vs AI mode.",
        "icon": "🤖"
    }
}

class AchievementManager:
    """
    Manages persistence of unlocked achievements and renders animated toast popups.
    """
    def __init__(self, sound_manager=None):
        self.sound_manager = sound_manager
        self.unlocked = set()
        self.active_toast = None  # Tuple: (key, timer_ticks)
        self.load_achievements()

    def load_achievements(self):
        """Loads unlocked achievement IDs from JSON storage."""
        if os.path.exists(ACHIEVEMENTS_FILE):
            try:
                with open(ACHIEVEMENTS_FILE, "r") as f:
                    data = json.load(f)
                    self.unlocked = set(data.get("unlocked", []))
            except Exception as e:
                print(f"[AchievementManager] Error loading achievements: {e}")

    def save_achievements(self):
        """Saves unlocked achievement IDs to JSON storage."""
        try:
            with open(ACHIEVEMENTS_FILE, "w") as f:
                json.dump({"unlocked": list(self.unlocked)}, f, indent=2)
        except Exception as e:
            print(f"[AchievementManager] Error saving achievements: {e}")

    def unlock(self, key):
        """
        Unlocks an achievement if not already earned.
        Triggers a sound effect and toast popup animation.
        """
        if key in ACHIEVEMENT_LIST and key not in self.unlocked:
            self.unlocked.add(key)
            self.save_achievements()
            self.active_toast = [key, 180]  # Display toast for 3 seconds (180 ticks @ 60fps)
            if self.sound_manager:
                self.sound_manager.play_achievement()

    def update(self):
        """Updates toast notification timer."""
        if self.active_toast:
            self.active_toast[1] -= 1
            if self.active_toast[1] <= 0:
                self.active_toast = None

    def draw_toast(self, surface):
        """Renders animated slide-down achievement toast popup at top of screen."""
        if not self.active_toast:
            return

        key, remaining = self.active_toast
        ach = ACHIEVEMENT_LIST[key]

        # Slide-in animation math
        total_time = 180
        elapsed = total_time - remaining
        
        if elapsed < 20:
            offset_y = -60 + (elapsed / 20.0) * 80  # Slide down into view at y=20
        elif remaining < 20:
            offset_y = 20 - ((20 - remaining) / 20.0) * 80 # Slide back up out of view
        else:
            offset_y = 20

        rect = pygame.Rect(WINDOW_WIDTH // 2 - 180, int(offset_y), 360, 50)
        
        # Toast Card Box
        toast_surf = pygame.Surface((360, 50), pygame.SRCALPHA)
        pygame.draw.rect(toast_surf, (15, 23, 42, 230), (0, 0, 360, 50), border_radius=10)
        pygame.draw.rect(toast_surf, ACCENT_GOLD, (0, 0, 360, 50), width=2, border_radius=10)

        # Render Text
        title_font = pygame.font.SysFont("Segoe UI", 14, bold=True)
        name_font = pygame.font.SysFont("Segoe UI", 12)

        header_str = "ACHIEVEMENT UNLOCKED!"
        header_lbl = title_font.render(header_str, True, ACCENT_GOLD)
        name_lbl = name_font.render(f"{ach['title']}: {ach['desc']}", True, TEXT_PRIMARY)

        toast_surf.blit(header_lbl, (15, 6))
        toast_surf.blit(name_lbl, (15, 26))

        surface.blit(toast_surf, rect.topleft)

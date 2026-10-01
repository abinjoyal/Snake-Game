import math
import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_DARK, PANEL_BG,
    TEXT_PRIMARY, TEXT_MUTED, ACCENT_GOLD, ACCENT_GREEN, ACCENT_BLUE
)
from ui.components import Button
from game.achievements import ACHIEVEMENT_LIST

class AchievementsScreen:
    """
    Renders the Hall of Fame Achievements gallery screen with vector badges and progress indicator.
    """
    def __init__(self, game_state_manager):
        self.gsm = game_state_manager
        btn_font = pygame.font.SysFont("Segoe UI", 16, bold=True)
        self.back_button = Button(
            (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 65, 200, 45),
            "BACK TO MENU",
            lambda: self._on_back_clicked(),
            btn_font,
            bg_color=(51, 65, 85),
            hover_color=(71, 85, 105),
            text_color=TEXT_PRIMARY
        )

    def _on_back_clicked(self):
        from game.game_state import State
        self.gsm.set_state(State.MENU)

    def handle_event(self, event):
        self.back_button.handle_event(event, self.gsm.sound_manager)

    def draw(self, surface):
        surface.fill(BG_DARK)

        # Header Title
        title_font = pygame.font.SysFont("Segoe UI", 32, bold=True)
        sub_font = pygame.font.SysFont("Segoe UI", 16)
        card_title_font = pygame.font.SysFont("Segoe UI", 16, bold=True)
        card_desc_font = pygame.font.SysFont("Segoe UI", 12)

        title_lbl = title_font.render("ACHIEVEMENTS & TROPHIES", True, ACCENT_GOLD)
        surface.blit(title_lbl, title_lbl.get_rect(center=(WINDOW_WIDTH // 2, 45)))

        unlocked_set = self.gsm.achievement_manager.unlocked
        total_count = len(ACHIEVEMENT_LIST)
        unlocked_count = len(unlocked_set)

        progress_str = f"Unlocked: {unlocked_count} / {total_count} ({int(unlocked_count/total_count*100)}%)"
        prog_lbl = sub_font.render(progress_str, True, TEXT_MUTED)
        surface.blit(prog_lbl, prog_lbl.get_rect(center=(WINDOW_WIDTH // 2, 80)))

        # 2-Column Grid Layout for Achievement Cards
        start_x = 60
        start_y = 110
        card_w = 320
        card_h = 75
        gap_x = 40
        gap_y = 18

        keys = list(ACHIEVEMENT_LIST.keys())
        for idx, key in enumerate(keys):
            row = idx // 2
            col = idx % 2
            cx = start_x + col * (card_w + gap_x)
            cy = start_y + row * (card_h + gap_y)

            card_rect = pygame.Rect(cx, cy, card_w, card_h)
            is_unlocked = key in unlocked_set
            ach_info = ACHIEVEMENT_LIST[key]

            # Card Background
            bg_col = (30, 41, 59) if is_unlocked else (20, 27, 40)
            border_col = ACCENT_GOLD if is_unlocked else (47, 63, 86)

            pygame.draw.rect(surface, bg_col, card_rect, border_radius=10)
            pygame.draw.rect(surface, border_col, card_rect, width=2 if is_unlocked else 1, border_radius=10)

            # Vector Badge Status Icon (Replaces font missing glyph box)
            icon_cx, icon_cy = cx + 26, cy + 37
            if is_unlocked:
                # Glowing Gold Unlocked Badge Circle
                pygame.draw.circle(surface, ACCENT_GOLD, (icon_cx, icon_cy), 13)
                # Checkmark
                pts = [(icon_cx - 5, icon_cy), (icon_cx - 1, icon_cy + 4), (icon_cx + 5, icon_cy - 4)]
                pygame.draw.lines(surface, (15, 23, 42), False, pts, 3)
            else:
                # Dark Locked Badge Circle
                pygame.draw.circle(surface, (47, 63, 86), (icon_cx, icon_cy), 13, width=2)
                # Lock Shackle Loop
                pygame.draw.arc(surface, (100, 116, 139), (icon_cx - 4, icon_cy - 7, 8, 8), 0, math.pi, 2)
                # Lock Body Box
                pygame.draw.rect(surface, (100, 116, 139), (icon_cx - 5, icon_cy - 1, 10, 7), border_radius=2)

            # Achievement Title & Description
            t_col = TEXT_PRIMARY if is_unlocked else (100, 116, 139)
            d_col = TEXT_MUTED if is_unlocked else (71, 85, 105)

            name_lbl = card_title_font.render(ach_info["title"], True, t_col)
            desc_lbl = card_desc_font.render(ach_info["desc"], True, d_col)

            surface.blit(name_lbl, (cx + 50, cy + 15))
            surface.blit(desc_lbl, (cx + 50, cy + 42))

        self.back_button.draw(surface)

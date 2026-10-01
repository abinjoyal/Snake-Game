import math
import colorsys
import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, PANEL_BG,
    TEXT_PRIMARY, TEXT_MUTED, ACCENT_GREEN, ACCENT_GOLD, SKINS
)
from ui.components import Button, draw_text, draw_text_glow
from game.game_state import State

class SkinsScreen:
    """
    Skins selection gallery allowing players to choose visual snake skins
    with a live wriggling animated preview box.
    """
    def __init__(self, game_state, title_font, font, small_font):
        self.game_state = game_state
        self.title_font = title_font
        self.font = font
        self.small_font = small_font

        self.preview_timer = 0

        # Build skin selection buttons
        self.skin_buttons = []
        skin_keys = list(SKINS.keys())
        
        start_y = 140
        spacing = 58
        btn_w, btn_h = 230, 48

        for i, key in enumerate(skin_keys):
            skin_name = SKINS[key]["name"]
            def make_callback(k=key):
                return lambda: self.game_state.set_skin(k)

            btn = Button(
                (50, start_y + i * spacing, btn_w, btn_h),
                skin_name,
                make_callback(key),
                font
            )
            self.skin_buttons.append((key, btn))

        # Back Button
        self.btn_back = Button(
            (WINDOW_WIDTH // 2 - 100, 535, 200, 44),
            "BACK TO MENU",
            lambda: self.game_state.set_state(State.MENU),
            font
        )

    def handle_event(self, event):
        """Dispatches event to skin cards and back button."""
        for key, btn in self.skin_buttons:
            btn.handle_event(event, self.game_state.sound_manager)
        self.btn_back.handle_event(event, self.game_state.sound_manager)

    def update(self):
        """Updates preview animation timer."""
        self.preview_timer += 1

    def draw(self, surface):
        """Renders skin selector UI and live preview."""
        surface.fill(BG_COLOR)

        # Header Title
        draw_text_glow(surface, "SNAKE SKINS", self.title_font, ACCENT_GREEN, (4, 120, 87), (WINDOW_WIDTH // 2, 55))
        draw_text(surface, "Choose your preferred snake aesthetic", self.small_font, TEXT_MUTED, (WINDOW_WIDTH // 2, 92))

        # Left Column: Skin Buttons List
        for key, btn in self.skin_buttons:
            is_active = (self.game_state.selected_skin == key)
            btn.border_color = ACCENT_GOLD if is_active else None
            btn.draw(surface)

            # Styled Pill Badge for Active Skin
            if is_active:
                badge_rect = pygame.Rect(295, btn.rect.y + 10, 95, 28)
                pygame.draw.rect(surface, (45, 35, 10), badge_rect, border_radius=14)
                pygame.draw.rect(surface, ACCENT_GOLD, badge_rect, width=1, border_radius=14)
                draw_text(surface, "EQUIPPED", self.small_font, ACCENT_GOLD, badge_rect.center, shadow=False)

        # Right Column: Live Snake Skin Preview Canvas Panel
        preview_panel = pygame.Rect(410, 140, 340, 340)
        pygame.draw.rect(surface, PANEL_BG, preview_panel, border_radius=12)
        pygame.draw.rect(surface, (50, 65, 85), preview_panel, width=1, border_radius=12)

        draw_text(surface, "LIVE PREVIEW", self.font, TEXT_PRIMARY, (preview_panel.centerx, preview_panel.y + 30))

        curr_skin_key = self.game_state.selected_skin
        curr_skin = SKINS.get(curr_skin_key, SKINS["classic"])
        draw_text(surface, curr_skin["description"], self.small_font, TEXT_MUTED, (preview_panel.centerx, preview_panel.y + 60))

        # Sub-surface preview canvas box
        box_w, box_h = 290, 200
        box_x = preview_panel.centerx - box_w // 2
        box_y = preview_panel.y + 95
        preview_box = pygame.Rect(box_x, box_y, box_w, box_h)

        preview_surface = pygame.Surface((box_w, box_h))
        preview_surface.fill((10, 15, 30))

        self._draw_preview_snake(preview_surface, curr_skin_key, curr_skin, box_w, box_h)

        surface.blit(preview_surface, preview_box.topleft)
        pygame.draw.rect(surface, ACCENT_GREEN, preview_box, width=2, border_radius=8)

        # Back Button
        self.btn_back.draw(surface)

    def _draw_preview_snake(self, surface, skin_key, skin_data, box_w, box_h):
        """Draws animated wriggling preview snake strictly within preview surface."""
        center_x = box_w // 2
        center_y = box_h // 2
        segment_size = 22
        t = self.preview_timer * 0.08

        for i in range(4, -1, -1):
            seg_x = center_x + (2 - i) * segment_size
            seg_y = center_y + int(math.sin(t - i * 0.4) * 14)
            rect = pygame.Rect(seg_x - segment_size // 2, seg_y - segment_size // 2, segment_size - 2, segment_size - 2)

            if i == 0:
                head_color = skin_data["head"]
                pygame.draw.rect(surface, head_color, rect, border_radius=6)
                
                eye_color = skin_data.get("eye_color", (255, 255, 255))
                pygame.draw.circle(surface, eye_color, (rect.right - 4, rect.top + 5), 2.5)
                pygame.draw.circle(surface, eye_color, (rect.right - 4, rect.bottom - 5), 2.5)
                pygame.draw.circle(surface, (10, 15, 30), (rect.right - 4, rect.top + 5), 1.2)
                pygame.draw.circle(surface, (10, 15, 30), (rect.right - 4, rect.bottom - 5), 1.2)
            else:
                if skin_key == "rainbow":
                    hue = (t * 0.2 + i * 0.15) % 1.0
                    r, g, b = colorsys.hsv_to_rgb(hue, 0.9, 0.95)
                    color = (int(r * 255), int(g * 255), int(b * 255))
                else:
                    ratio = i / 5.0
                    start_c = skin_data["body_start"]
                    end_c = skin_data["body_end"]
                    color = (
                        int(start_c[0] + (end_c[0] - start_c[0]) * ratio),
                        int(start_c[1] + (end_c[1] - start_c[1]) * ratio),
                        int(start_c[2] + (end_c[2] - start_c[2]) * ratio)
                    )

                pygame.draw.rect(surface, color, rect, border_radius=4)

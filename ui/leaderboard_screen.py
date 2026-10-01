import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR, PANEL_BG,
    TEXT_PRIMARY, TEXT_MUTED, ACCENT_GOLD, ACCENT_GREEN
)
from ui.components import Button, draw_text, draw_text_glow
from game.game_state import State

class LeaderboardScreen:
    """
    Leaderboard screen rendering top 10 historical scores in a clean table format.
    """
    def __init__(self, game_state, title_font, font, small_font):
        self.game_state = game_state
        self.title_font = title_font
        self.font = font
        self.small_font = small_font

        # Back Button
        btn_w, btn_h = 200, 44
        self.btn_back = Button(
            (WINDOW_WIDTH // 2 - btn_w // 2, 535, btn_w, btn_h),
            "BACK TO MENU",
            lambda: self.game_state.set_state(State.MENU),
            font
        )

    def handle_event(self, event):
        """Dispatches event to back button."""
        self.btn_back.handle_event(event, self.game_state.sound_manager)

    def draw(self, surface):
        """Renders leaderboard table and records."""
        surface.fill(BG_COLOR)

        # Screen Title
        draw_text_glow(surface, "HALL OF FAME", self.title_font, ACCENT_GOLD, (180, 83, 9), (WINDOW_WIDTH // 2, 55))
        draw_text(surface, "Top 10 High Scores", self.small_font, TEXT_MUTED, (WINDOW_WIDTH // 2, 92))

        # Main Table Container Panel
        panel_w, panel_h = 650, 395
        panel_rect = pygame.Rect(WINDOW_WIDTH // 2 - panel_w // 2, 118, panel_w, panel_h)
        pygame.draw.rect(surface, PANEL_BG, panel_rect, border_radius=12)
        pygame.draw.rect(surface, (50, 65, 85), panel_rect, width=1, border_radius=12)

        # Table Header Row
        header_y = 142
        draw_text(surface, "RANK", self.small_font, ACCENT_GOLD, (panel_rect.x + 50, header_y))
        draw_text(surface, "PLAYER NAME", self.small_font, ACCENT_GOLD, (panel_rect.x + 200, header_y))
        draw_text(surface, "SCORE", self.small_font, ACCENT_GOLD, (panel_rect.x + 390, header_y))
        draw_text(surface, "DATE", self.small_font, ACCENT_GOLD, (panel_rect.x + 540, header_y))

        pygame.draw.line(surface, (50, 65, 85), (panel_rect.x + 20, 162), (panel_rect.right - 20, 162), 1)

        # Retrieve Scores List
        scores = self.game_state.leaderboard_manager.get_top_scores(limit=10)

        if not scores:
            draw_text(surface, "No scores recorded yet. Play a game to set a record!",
                      self.font, TEXT_MUTED, (WINDOW_WIDTH // 2, 300))
        else:
            row_y = 188
            for index, record in enumerate(scores):
                rank = index + 1
                name = record.get("name", "Player")
                score_val = record.get("score", 0)
                date_str = record.get("date", "")

                if rank == 1:
                    rank_str = "Rank #1"
                    rank_color = ACCENT_GOLD
                elif rank == 2:
                    rank_str = "Rank #2"
                    rank_color = (203, 213, 225)
                elif rank == 3:
                    rank_str = "Rank #3"
                    rank_color = (217, 119, 6)
                else:
                    rank_str = f"Rank #{rank}"
                    rank_color = TEXT_MUTED

                draw_text(surface, rank_str, self.small_font, rank_color, (panel_rect.x + 50, row_y))
                draw_text(surface, name, self.small_font, TEXT_PRIMARY, (panel_rect.x + 200, row_y))
                draw_text(surface, str(score_val), self.small_font, ACCENT_GREEN, (panel_rect.x + 390, row_y))
                draw_text(surface, date_str, self.small_font, TEXT_MUTED, (panel_rect.x + 540, row_y))

                row_y += 32

        # Draw Back Button
        self.btn_back.draw(surface)

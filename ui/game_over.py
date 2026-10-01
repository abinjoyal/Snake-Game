import pygame
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, PANEL_BG, TEXT_PRIMARY,
    TEXT_MUTED, ACCENT_RED, ACCENT_GREEN, ACCENT_GOLD, ACCENT_BLUE
)
from ui.components import Button, TextInput, draw_text
from game.game_state import State

class GameOverScreen:
    """
    Game Over UI screen displaying final scores, 2P / VS_AI winner announcement,
    high score celebration, player name input, and restart options.
    """
    def __init__(self, game_state, title_font, font, small_font):
        self.game_state = game_state
        self.title_font = title_font
        self.font = font
        self.small_font = small_font

        panel_w, panel_h = 460, 490
        self.panel_rect = pygame.Rect(
            (WINDOW_WIDTH // 2 - panel_w // 2, WINDOW_HEIGHT // 2 - panel_h // 2),
            (panel_w, panel_h)
        )

        input_w, input_h = 300, 44
        input_x = WINDOW_WIDTH // 2 - input_w // 2
        input_y = self.panel_rect.y + 250
        self.name_input = TextInput((input_x, input_y, input_w, input_h), font, max_length=12)

        btn_w, btn_h = 300, 42
        btn_x = WINDOW_WIDTH // 2 - btn_w // 2
        btn_y = self.panel_rect.y + 310
        spacing = 50

        self.btn_submit = Button((btn_x, btn_y, btn_w, btn_h), "SAVE SCORE TO LEADERBOARD",
                                 self._submit_score, small_font, hover_color=ACCENT_GOLD)
        self.btn_play_again = Button((btn_x, btn_y + spacing, btn_w, btn_h), "PLAY AGAIN",
                                     lambda: self.game_state.start_new_game(), small_font, hover_color=ACCENT_GREEN)
        self.btn_menu = Button((btn_x, btn_y + spacing * 2, btn_w, btn_h), "MAIN MENU",
                               lambda: self.game_state.set_state(State.MENU), small_font)

        self.score_submitted = False

    def reset_submission(self):
        """Resets name input state when game over screen opens."""
        self.score_submitted = False
        self.name_input.text = ""

    def _submit_score(self):
        """Saves player score to local leaderboard JSON."""
        if self.score_submitted:
            self.game_state.set_state(State.LEADERBOARD)
            return

        name = self.name_input.text.strip() or "Player"
        self.game_state.leaderboard_manager.add_score(name, self.game_state.score)
        self.score_submitted = True
        self.game_state.set_state(State.LEADERBOARD)

    def handle_event(self, event):
        """Dispatches input events to name input widget and buttons."""
        if self.game_state.game_mode == "1P" and not self.score_submitted:
            if self.name_input.handle_event(event):
                self._submit_score()
                return

        if self.game_state.game_mode == "1P":
            self.btn_submit.handle_event(event, self.game_state.sound_manager)
        self.btn_play_again.handle_event(event, self.game_state.sound_manager)
        self.btn_menu.handle_event(event, self.game_state.sound_manager)

    def update(self):
        """Updates cursor animation."""
        self.name_input.update()

    def draw(self, surface):
        """Renders Game Over panel overlay."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 15, 30, 180))
        surface.blit(overlay, (0, 0))

        # Panel Body
        pygame.draw.rect(surface, PANEL_BG, self.panel_rect, border_radius=16)
        pygame.draw.rect(surface, ACCENT_RED, self.panel_rect, width=2, border_radius=16)

        cx = WINDOW_WIDTH // 2
        top_y = self.panel_rect.y + 35

        # Header Title
        draw_text(surface, "GAME OVER", self.title_font, ACCENT_RED, (cx, top_y))

        if self.game_state.game_mode in ("2P", "VS_AI"):
            # 2-Player / VS_AI Winner Announcement Banner
            draw_text(surface, self.game_state.winner_text, self.font, ACCENT_GOLD, (cx, top_y + 50))
            score_p2_label = "BOT" if self.game_state.game_mode == "VS_AI" else "P2"
            draw_text(surface, f"YOU: {self.game_state.score}  |  {score_p2_label}: {self.game_state.score_p2}",
                      self.font, TEXT_PRIMARY, (cx, top_y + 95))
            
            # Render Play Again & Main Menu buttons
            self.btn_play_again.rect.y = self.panel_rect.y + 240
            self.btn_menu.rect.y = self.panel_rect.y + 300
            self.btn_play_again.draw(surface)
            self.btn_menu.draw(surface)
        else:
            # 1-Player Solo Summary
            if self.game_state.is_new_high_score:
                draw_text(surface, "NEW HIGH SCORE!", self.font, ACCENT_GOLD, (cx, top_y + 45))

            score_y = top_y + (80 if self.game_state.is_new_high_score else 65)
            draw_text(surface, f"FINAL SCORE: {self.game_state.score}", self.font, TEXT_PRIMARY, (cx, score_y))
            
            high_score = self.game_state.leaderboard_manager.get_high_score()
            draw_text(surface, f"BEST HIGH SCORE: {high_score}", self.small_font, TEXT_MUTED, (cx, score_y + 35))

            if not self.score_submitted:
                draw_text(surface, "Enter Player Name:", self.small_font, TEXT_PRIMARY, (cx, score_y + 70))
                self.name_input.draw(surface)
                self.btn_submit.rect.y = self.panel_rect.y + 310
                self.btn_submit.draw(surface)
            else:
                draw_text(surface, "Score Saved to Leaderboard!", self.small_font, ACCENT_GREEN, (cx, score_y + 80))

            self.btn_play_again.rect.y = self.panel_rect.y + 360
            self.btn_menu.rect.y = self.panel_rect.y + 410
            self.btn_play_again.draw(surface)
            self.btn_menu.draw(surface)

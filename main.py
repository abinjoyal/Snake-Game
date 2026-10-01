import sys
import pygame

from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, BG_COLOR,
    GRID_LINE_COLOR, GRID_SIZE, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT_GREEN, ACCENT_GOLD, ACCENT_RED, ACCENT_BLUE, PANEL_BG,
    MAZE_OBSTACLES, GRID_WIDTH, GRID_HEIGHT
)

from game.game_state import GameStateManager, State
from game.collision import (
    check_wall_collision, check_obstacle_collision,
    check_self_collision, check_food_collision,
    check_snake_vs_snake_collision
)

from ui.menu import MainMenuScreen
from ui.game_over import GameOverScreen
from ui.leaderboard_screen import LeaderboardScreen
from ui.skins_screen import SkinsScreen
from ui.settings_screen import SettingsScreen
from ui.achievements_screen import AchievementsScreen
from ui.map_builder_screen import MapBuilderScreen
from ui.components import draw_text, Button

class SnakeGame:
    """
    Main Game Application managing window initialization, event routing,
    1P/2P/VS_AI controls, particle effects, shield protections, and game loop.
    """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Classic Snake Game")

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize Fonts
        self.title_font = pygame.font.SysFont("Segoe UI", 44, bold=True)
        self.font = pygame.font.SysFont("Segoe UI", 24, bold=True)
        self.small_font = pygame.font.SysFont("Segoe UI", 16, bold=True)

        # Initialize Core State Manager
        self.game_state = GameStateManager()

        # Initialize UI Screens
        self.menu_screen = MainMenuScreen(
            self.game_state, self.title_font, self.font, self.small_font, self.quit_game
        )
        self.game_over_screen = GameOverScreen(
            self.game_state, self.title_font, self.font, self.small_font
        )
        self.leaderboard_screen = LeaderboardScreen(
            self.game_state, self.title_font, self.font, self.small_font
        )
        self.skins_screen = SkinsScreen(
            self.game_state, self.title_font, self.font, self.small_font
        )
        self.settings_screen = SettingsScreen(
            self.game_state, self.title_font, self.font, self.small_font
        )
        self.achievements_screen = AchievementsScreen(self.game_state)
        self.map_builder_screen = MapBuilderScreen(self.game_state)

        self.last_move_time = 0

        # Pause Overlay Buttons
        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2
        self.pause_btn_resume = Button((cx - 100, cy - 15, 200, 44), "RESUME",
                                       self.game_state.toggle_pause, self.font, hover_color=ACCENT_GREEN)
        self.pause_btn_menu = Button((cx - 100, cy + 45, 200, 44), "MAIN MENU",
                                     lambda: self.game_state.set_state(State.MENU), self.font)

    def quit_game(self):
        """Cleanly closes application."""
        self.running = False

    def run(self):
        """Main Application Loop."""
        while self.running:
            dt = self.clock.tick(FPS)
            self.game_state.tick_count += 1
            current_time = pygame.time.get_ticks()

            self._handle_events()
            self._update(current_time)
            self._draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        """Dispatches keyboard and mouse events depending on active state."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if self.game_state.state == State.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if self.game_state.game_mode in ("1P", "VS_AI"):
                        if event.key in (pygame.K_UP, pygame.K_w):
                            self.game_state.snake.set_direction((0, -1))
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            self.game_state.snake.set_direction((0, 1))
                        elif event.key in (pygame.K_LEFT, pygame.K_a):
                            self.game_state.snake.set_direction((-1, 0))
                        elif event.key in (pygame.K_RIGHT, pygame.K_d):
                            self.game_state.snake.set_direction((1, 0))
                    elif self.game_state.game_mode == "2P":
                        if event.key == pygame.K_w:
                            self.game_state.snake.set_direction((0, -1))
                        elif event.key == pygame.K_s:
                            self.game_state.snake.set_direction((0, 1))
                        elif event.key == pygame.K_a:
                            self.game_state.snake.set_direction((-1, 0))
                        elif event.key == pygame.K_d:
                            self.game_state.snake.set_direction((1, 0))

                        if event.key == pygame.K_UP:
                            self.game_state.snake2.set_direction((0, -1))
                        elif event.key == pygame.K_DOWN:
                            self.game_state.snake2.set_direction((0, 1))
                        elif event.key == pygame.K_LEFT:
                            self.game_state.snake2.set_direction((-1, 0))
                        elif event.key == pygame.K_RIGHT:
                            self.game_state.snake2.set_direction((1, 0))

                    if event.key in (pygame.K_p, pygame.K_ESCAPE):
                        self.game_state.toggle_pause()
                    elif event.key == pygame.K_r:
                        self.game_state.start_new_game()

            elif self.game_state.state == State.PAUSED:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_p, pygame.K_ESCAPE):
                        self.game_state.toggle_pause()
                self.pause_btn_resume.handle_event(event, self.game_state.sound_manager)
                self.pause_btn_menu.handle_event(event, self.game_state.sound_manager)

            elif self.game_state.state == State.MENU:
                self.menu_screen.handle_event(event)

            elif self.game_state.state == State.GAME_OVER:
                self.game_over_screen.handle_event(event)

            elif self.game_state.state == State.LEADERBOARD:
                self.leaderboard_screen.handle_event(event)

            elif self.game_state.state == State.SKINS:
                self.skins_screen.handle_event(event)

            elif self.game_state.state == State.SETTINGS:
                self.settings_screen.handle_event(event)

            elif self.game_state.state == State.ACHIEVEMENTS:
                self.achievements_screen.handle_event(event)

            elif self.game_state.state == State.MAP_BUILDER:
                self.map_builder_screen.handle_event(event)

    def _update(self, current_time):
        """Executes gameplay tick movement, AI logic, powerup timers, and collision logic."""
        if self.game_state.state == State.PLAYING:
            self.game_state.update_timers()
            
            food_expired = self.game_state.food.update()
            if food_expired:
                p2_body = self.game_state.snake2.body if self.game_state.game_mode == "2P" else (self.game_state.ai_snake.body if self.game_state.game_mode == "VS_AI" else [])
                self.game_state.food.respawn(self.game_state.snake.body + p2_body, self.game_state.map_mode)

            effective_speed = self.game_state.get_effective_speed()
            move_delay = 1000 // effective_speed

            if current_time - self.last_move_time >= move_delay:
                self.last_move_time = current_time
                is_portal = (self.game_state.map_mode == "PORTAL")

                head1 = self.game_state.snake.update(wrap_portal=is_portal, grid_width=GRID_WIDTH, grid_height=GRID_HEIGHT)

                head2 = None
                if self.game_state.game_mode == "2P":
                    head2 = self.game_state.snake2.update(wrap_portal=is_portal, grid_width=GRID_WIDTH, grid_height=GRID_HEIGHT)
                elif self.game_state.game_mode == "VS_AI":
                    # Update AI Bot pathfinding towards food
                    obstacles = list(self.game_state.snake.body)
                    if self.game_state.map_mode == "OBSTACLES":
                        obstacles.extend(list(MAZE_OBSTACLES))
                    elif self.game_state.map_mode == "CUSTOM":
                        obstacles.extend(list(self.game_state.custom_obstacles))
                    self.game_state.ai_snake.update_ai_direction(self.game_state.food.position, obstacles)
                    head2 = self.game_state.ai_snake.update(wrap_portal=is_portal, grid_width=GRID_WIDTH, grid_height=GRID_HEIGHT)

                # Collision Checks for Snake 1
                cust_obs = self.game_state.custom_obstacles if self.game_state.map_mode in ("CUSTOM", "CAMPAIGN") else None
                loser1 = (
                    check_wall_collision(head1, self.game_state.map_mode) or
                    check_obstacle_collision(head1, self.game_state.map_mode, custom_obstacles=cust_obs) or
                    check_self_collision(head1, self.game_state.snake.body)
                )

                # Handle Shield Bubble Absorption for Snake 1
                if loser1 and self.game_state.snake.shield_active:
                    self.game_state.snake.pop_shield()
                    self.game_state.sound_manager.play_shield_pop()
                    self.game_state.achievement_manager.unlock("SHIELD_SAVE")
                    # Push snake back 1 tile to prevent clipping
                    self.game_state.snake.body.pop(0)
                    loser1 = False

                loser2 = False
                if self.game_state.game_mode == "2P":
                    loser2 = (
                        check_wall_collision(head2, self.game_state.map_mode) or
                        check_obstacle_collision(head2, self.game_state.map_mode, custom_obstacles=cust_obs) or
                        check_self_collision(head2, self.game_state.snake2.body) or
                        check_snake_vs_snake_collision(head1, self.game_state.snake2.body) or
                        check_snake_vs_snake_collision(head2, self.game_state.snake.body)
                    )
                elif self.game_state.game_mode == "VS_AI":
                    loser2 = (
                        check_wall_collision(head2, self.game_state.map_mode) or
                        check_obstacle_collision(head2, self.game_state.map_mode, custom_obstacles=cust_obs) or
                        check_self_collision(head2, self.game_state.ai_snake.body) or
                        check_snake_vs_snake_collision(head1, self.game_state.ai_snake.body) or
                        check_snake_vs_snake_collision(head2, self.game_state.snake.body)
                    )

                if loser1 or loser2:
                    self.game_state.trigger_game_over(loser1, loser2)
                    self.game_over_screen.reset_submission()
                    return

                if check_food_collision(head1, self.game_state.food.position):
                    self.game_state.handle_food_eaten(self.game_state.snake, is_player_2=False)

                if self.game_state.game_mode == "2P" and head2 is not None:
                    if check_food_collision(head2, self.game_state.food.position):
                        self.game_state.handle_food_eaten(self.game_state.snake2, is_player_2=True)
                elif self.game_state.game_mode == "VS_AI" and head2 is not None:
                    if check_food_collision(head2, self.game_state.food.position):
                        self.game_state.handle_food_eaten(self.game_state.ai_snake, is_player_2=True)

        elif self.game_state.state == State.MENU:
            self.menu_screen.update()

        elif self.game_state.state == State.SKINS:
            self.skins_screen.update()

        elif self.game_state.state == State.GAME_OVER:
            self.game_over_screen.update()

    def _draw(self):
        """Renders scene with screen shake offset."""
        shake_x, shake_y = self.game_state.particle_manager.shake_offset
        
        canvas = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        canvas.fill(BG_COLOR)
        self._draw_grid_to_canvas(canvas)

        if self.game_state.state in (State.PLAYING, State.PAUSED):
            if self.game_state.map_mode == "OBSTACLES":
                self._draw_obstacles(canvas)
            elif self.game_state.map_mode in ("CUSTOM", "CAMPAIGN"):
                self._draw_custom_obstacles(canvas)

            self.game_state.food.draw(canvas)
            self.game_state.snake.draw(canvas, tick_count=self.game_state.tick_count)
            
            if self.game_state.game_mode == "2P":
                self.game_state.snake2.draw(canvas, tick_count=self.game_state.tick_count)
            elif self.game_state.game_mode == "VS_AI":
                self.game_state.ai_snake.draw(canvas, tick_count=self.game_state.tick_count)

            self.game_state.particle_manager.draw(canvas)
            self._draw_hud(canvas)
            self.game_state.achievement_manager.draw_toast(canvas)

            if self.game_state.state == State.PAUSED:
                self._draw_pause_overlay(canvas)

        elif self.game_state.state == State.MENU:
            self.menu_screen.draw(canvas)

        elif self.game_state.state == State.GAME_OVER:
            if self.game_state.map_mode == "OBSTACLES":
                self._draw_obstacles(canvas)
            elif self.game_state.map_mode in ("CUSTOM", "CAMPAIGN"):
                self._draw_custom_obstacles(canvas)
            self.game_state.food.draw(canvas)
            self.game_state.snake.draw(canvas)
            if self.game_state.game_mode == "2P":
                self.game_state.snake2.draw(canvas)
            elif self.game_state.game_mode == "VS_AI":
                self.game_state.ai_snake.draw(canvas)
            self.game_state.particle_manager.draw(canvas)
            self._draw_hud(canvas)
            self.game_over_screen.draw(canvas)

        elif self.game_state.state == State.LEADERBOARD:
            self.leaderboard_screen.draw(canvas)

        elif self.game_state.state == State.SKINS:
            self.skins_screen.draw(canvas)

        elif self.game_state.state == State.SETTINGS:
            self.settings_screen.draw(canvas)

        elif self.game_state.state == State.ACHIEVEMENTS:
            self.achievements_screen.draw(canvas)

        elif self.game_state.state == State.MAP_BUILDER:
            self.map_builder_screen.draw(canvas)

        self.screen.blit(canvas, (shake_x, shake_y))

    def _draw_grid_to_canvas(self, surface):
        """Renders grid lines."""
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(surface, GRID_LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, GRID_LINE_COLOR, (0, y), (WINDOW_WIDTH, y))

    def _draw_obstacles(self, surface):
        """Renders brick obstacles for Maze map mode."""
        for gx, gy in MAZE_OBSTACLES:
            rect = pygame.Rect(gx * GRID_SIZE + 1, gy * GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2)
            pygame.draw.rect(surface, (71, 85, 105), rect, border_radius=4)
            pygame.draw.rect(surface, (100, 116, 139), rect, width=2, border_radius=4)

    def _draw_custom_obstacles(self, surface):
        """Renders brick obstacles for Custom/Campaign map modes."""
        for gx, gy in self.game_state.custom_obstacles:
            rect = pygame.Rect(gx * GRID_SIZE + 1, gy * GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2)
            pygame.draw.rect(surface, (148, 163, 184), rect, border_radius=4)
            pygame.draw.rect(surface, (71, 85, 105), rect, width=2, border_radius=4)

    def _draw_hud(self, surface):
        """Renders HUD bar with scores, level, combo badge, and active powerup status."""
        hud_height = 42
        hud_surface = pygame.Surface((WINDOW_WIDTH, hud_height), pygame.SRCALPHA)
        hud_surface.fill((10, 15, 30, 210))
        surface.blit(hud_surface, (0, 0))

        if self.game_state.game_mode == "2P":
            p1_text = f"P1 SCORE: {self.game_state.score}"
            p2_text = f"P2 SCORE: {self.game_state.score_p2}"
            draw_text(surface, p1_text, self.small_font, ACCENT_GREEN, (100, 21), shadow=False)
            draw_text(surface, p2_text, self.small_font, ACCENT_BLUE, (270, 21), shadow=False)
        elif self.game_state.game_mode == "VS_AI":
            p1_text = f"YOU: {self.game_state.score}"
            bot_text = f"BOT: {self.game_state.score_p2}"
            draw_text(surface, p1_text, self.small_font, ACCENT_GREEN, (80, 21), shadow=False)
            draw_text(surface, bot_text, self.small_font, ACCENT_BLUE, (220, 21), shadow=False)
        else:
            high_score = self.game_state.leaderboard_manager.get_high_score()
            score_text = f"SCORE: {self.game_state.score}"
            high_text = f"HIGH SCORE: {high_score}"
            draw_text(surface, score_text, self.small_font, ACCENT_GREEN, (80, 21), shadow=False)
            draw_text(surface, high_text, self.small_font, ACCENT_GOLD, (240, 21), shadow=False)

        if self.game_state.map_mode == "CAMPAIGN":
            lvl_text = f"LEVEL {self.game_state.campaign_level}"
            draw_text(surface, lvl_text, self.small_font, ACCENT_PURPLE, (360, 21), shadow=False)

        if self.game_state.multiplier > 1:
            combo_badge = f"{self.game_state.multiplier}x COMBO!"
            draw_text(surface, combo_badge, self.small_font, ACCENT_GOLD, (460, 21), shadow=False)

        if self.game_state.speed_boost_timer > 0:
            draw_text(surface, "SPEED BOOST", self.small_font, ACCENT_BLUE, (580, 21), shadow=False)
        elif self.game_state.slow_mo_timer > 0:
            draw_text(surface, "SLOW-MO", self.small_font, (6, 182, 212), (580, 21), shadow=False)
        elif self.game_state.magnet_timer > 0:
            draw_text(surface, "MAGNET", self.small_font, (234, 179, 8), (580, 21), shadow=False)

        draw_text(surface, "[P] PAUSE", self.small_font, TEXT_MUTED, (WINDOW_WIDTH - 65, 21), shadow=False)

    def _draw_pause_overlay(self, surface):
        """Renders pause menu overlay."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 15, 30, 160))
        surface.blit(overlay, (0, 0))

        cx = WINDOW_WIDTH // 2
        cy = WINDOW_HEIGHT // 2

        card_rect = pygame.Rect(cx - 200, cy - 120, 400, 240)
        pygame.draw.rect(surface, PANEL_BG, card_rect, border_radius=12)
        pygame.draw.rect(surface, ACCENT_GREEN, card_rect, width=2, border_radius=12)

        draw_text(surface, "GAME PAUSED", self.title_font, ACCENT_GREEN, (cx, cy - 65))
        self.pause_btn_resume.draw(surface)
        self.pause_btn_menu.draw(surface)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()

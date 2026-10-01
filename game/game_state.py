import os
import json
from collections import deque
from enum import Enum, auto
from game.snake import Snake
from game.ai_snake import AISnake
from game.food import Food
from game.sound_manager import SoundManager
from game.leaderboard import LeaderboardManager
from game.particle import ParticleManager
from game.achievements import AchievementManager
from settings import DEFAULT_SPEED, GRID_SIZE, CUSTOM_MAP_FILE, MAZE_OBSTACLES

class State(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    LEADERBOARD = auto()
    SKINS = auto()
    SETTINGS = auto()
    ACHIEVEMENTS = auto()
    MAP_BUILDER = auto()

class GameStateManager:
    """
    Central Game Manager coordinating 1P/2P/VS_AI game modes, map modes,
    combos, magnet & shield powerups, campaign levels, replay history, and achievements.
    """
    def __init__(self):
        self.state = State.MENU
        self.sound_manager = SoundManager()
        self.leaderboard_manager = LeaderboardManager()
        self.particle_manager = ParticleManager()
        self.achievement_manager = AchievementManager(self.sound_manager)
        
        # Game Options
        self.game_mode = "1P"          # "1P", "2P", "VS_AI"
        self.map_mode = "CLASSIC"       # "CLASSIC", "PORTAL", "OBSTACLES", "CAMPAIGN", "CUSTOM"
        self.selected_skin = "classic"
        self.selected_skin_p2 = "blue"
        self.game_speed = DEFAULT_SPEED
        self.tick_count = 0

        # Custom Map & Campaign Obstacles
        self.custom_obstacles = set()
        self.load_custom_map()

        # Entities
        self.snake = Snake(start_x=10, start_y=12, skin_key="classic")
        self.snake2 = Snake(start_x=22, start_y=12, default_dir=(-1, 0), skin_key="blue")
        self.ai_snake = AISnake(start_x=22, start_y=12, default_dir=(-1, 0), skin_key="blue")

        self.food = Food()
        self.food.respawn(self.snake.body, self.map_mode)

        # Scoring, Combos & Campaign Level
        self.score = 0
        self.score_p2 = 0
        self.combo_count = 0
        self.combo_timer = 0
        self.multiplier = 1
        self.campaign_level = 1
        self.is_new_high_score = False
        self.winner_text = ""

        # Active Power-Up Timers
        self.speed_boost_timer = 0
        self.slow_mo_timer = 0
        self.magnet_timer = 0

        # Death Replay Frame Buffer (Stores last 20 snake position snapshots)
        self.replay_buffer = deque(maxlen=20)

    def load_custom_map(self):
        """Loads user-created obstacle tiles from disk."""
        if os.path.exists(CUSTOM_MAP_FILE):
            try:
                with open(CUSTOM_MAP_FILE, "r") as f:
                    data = json.load(f)
                    self.custom_obstacles = set(tuple(p) for p in data.get("obstacles", []))
            except Exception as e:
                print(f"[GameStateManager] Error loading custom map: {e}")

    def start_new_game(self):
        """Resets game session state for 1P, 2P, or VS_AI play."""
        self.load_custom_map()
        self.snake.reset()
        self.snake.set_skin(self.selected_skin)
        
        if self.game_mode == "2P":
            self.snake2.reset()
            self.snake2.set_skin(self.selected_skin_p2)
        elif self.game_mode == "VS_AI":
            self.ai_snake.reset()

        active_snake2 = self.snake2.body if self.game_mode == "2P" else (self.ai_snake.body if self.game_mode == "VS_AI" else [])
        self.food.respawn(self.snake.body + active_snake2, self.map_mode)
        
        self.score = 0
        self.score_p2 = 0
        self.combo_count = 0
        self.combo_timer = 0
        self.multiplier = 1
        self.campaign_level = 1
        self.is_new_high_score = False
        self.winner_text = ""
        self.speed_boost_timer = 0
        self.slow_mo_timer = 0
        self.magnet_timer = 0
        self.replay_buffer.clear()
        
        self.sound_manager.start_bgm()
        self.state = State.PLAYING

    def set_state(self, new_state):
        """Transitions active game state."""
        self.state = new_state
        if new_state != State.PLAYING:
            self.sound_manager.stop_bgm()

    def toggle_pause(self):
        """Toggles between PLAYING and PAUSED states."""
        if self.state == State.PLAYING:
            self.sound_manager.play_pause()
            self.sound_manager.stop_bgm()
            self.state = State.PAUSED
        elif self.state == State.PAUSED:
            self.sound_manager.play_pause()
            self.sound_manager.start_bgm()
            self.state = State.PLAYING

    def update_timers(self):
        """Updates powerup effect timers, magnet physics, and combo countdowns."""
        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer == 0:
                self.combo_count = 0
                self.multiplier = 1

        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1

        if self.slow_mo_timer > 0:
            self.slow_mo_timer -= 1

        if self.magnet_timer > 0:
            self.magnet_timer -= 1
            # Magnet Attraction Physics: pull food 1 tile closer to snake head every 6 frames
            if self.tick_count % 6 == 0:
                hx, hy = self.snake.body[0]
                fx, fy = self.food.position
                if hx < fx: fx -= 1
                elif hx > fx: fx += 1
                elif hy < fy: fy -= 1
                elif hy > fy: fy += 1
                self.food.position = (fx, fy)

        self.particle_manager.update()
        self.achievement_manager.update()

    def get_effective_speed(self):
        """Calculates current game speed adjusted for campaign levels & active powerups."""
        base = self.game_speed
        if self.map_mode == "CAMPAIGN":
            base += (self.campaign_level - 1) * 2  # Increase speed per level

        if self.speed_boost_timer > 0:
            return int(base * 1.5)
        elif self.slow_mo_timer > 0:
            return max(5, int(base * 0.7))
        return base

    def handle_food_eaten(self, eating_snake, is_player_2=False):
        """Handles point calculation, combo multipliers, sound effects, powerups, and achievements."""
        food_type = self.food.type_key
        base_points = self.food.type_info["points"]
        grow_val = self.food.type_info["grow"]

        if grow_val > 0:
            eating_snake.grow(grow_val)
        elif grow_val < 0:
            eating_snake.shrink(abs(grow_val))

        self.combo_count += 1
        self.combo_timer = 210
        self.multiplier = min(5, 1 + self.combo_count // 2)

        earned_points = base_points * self.multiplier

        if is_player_2:
            self.score_p2 += earned_points
        else:
            self.score += earned_points
            # Campaign Mode Level Up
            if self.map_mode == "CAMPAIGN":
                new_level = 1 + self.score // 100
                if new_level > self.campaign_level:
                    self.campaign_level = new_level
                    self.sound_manager.play_achievement()

        # Check Achievements
        if not is_player_2:
            self.achievement_manager.unlock("FIRST_EAT")
            if self.multiplier >= 3:
                self.achievement_manager.unlock("COMBO_3")
            if self.multiplier >= 5:
                self.achievement_manager.unlock("COMBO_5")
            if self.score >= 100:
                self.achievement_manager.unlock("SCORE_100")
            if self.score >= 300:
                self.achievement_manager.unlock("SCORE_300")

        fx, fy = self.food.position
        pixel_x = fx * GRID_SIZE + GRID_SIZE // 2
        pixel_y = fy * GRID_SIZE + GRID_SIZE // 2

        color = self.food.type_info["color"]
        self.particle_manager.add_burst(pixel_x, pixel_y, color, count=18)

        if food_type == "GOLDEN":
            self.sound_manager.play_powerup()
            self.particle_manager.add_gold_sparkles(pixel_x, pixel_y, count=12)
        elif food_type == "SPEED_BOOST":
            self.sound_manager.play_powerup()
            self.speed_boost_timer = 300
        elif food_type == "SLOW_MO":
            self.sound_manager.play_powerup()
            self.slow_mo_timer = 300
        elif food_type == "MAGNET":
            self.sound_manager.play_powerup()
            self.magnet_timer = 300
            if not is_player_2:
                self.achievement_manager.unlock("MAGNET_MASTER")
        elif food_type == "SHIELD":
            self.sound_manager.play_powerup()
            eating_snake.activate_shield()
        else:
            if self.multiplier > 1:
                self.sound_manager.play_combo()
            else:
                self.sound_manager.play_eat()

        active_p2_body = self.snake2.body if self.game_mode == "2P" else (self.ai_snake.body if self.game_mode == "VS_AI" else [])
        occupied = self.snake.body + active_p2_body
        self.food.respawn(occupied, self.map_mode)

    def trigger_game_over(self, loser_p1=False, loser_p2=False):
        """Handles transition into Game Over state with screen shake, winner logic, and BGM stop."""
        self.sound_manager.play_gameover()
        self.particle_manager.trigger_screen_shake(12)

        if self.game_mode == "2P":
            if loser_p1 and loser_p2:
                self.winner_text = "IT'S A DRAW!"
            elif loser_p1:
                self.winner_text = "PLAYER 2 WINS!"
            elif loser_p2:
                self.winner_text = "PLAYER 1 WINS!"
            else:
                if self.score > self.score_p2:
                    self.winner_text = "PLAYER 1 WINS!"
                elif self.score_p2 > self.score:
                    self.winner_text = "PLAYER 2 WINS!"
                else:
                    self.winner_text = "IT'S A DRAW!"
        elif self.game_mode == "VS_AI":
            if loser_p1 and loser_p2:
                self.winner_text = "IT'S A DRAW!"
            elif loser_p1:
                self.winner_text = "AI BOT WINS!"
            elif loser_p2:
                self.winner_text = "YOU DEFEATED THE BOT!"
                self.achievement_manager.unlock("BOT_BUSTER")
            else:
                if self.score > self.score_p2:
                    self.winner_text = "YOU DEFEATED THE BOT!"
                    self.achievement_manager.unlock("BOT_BUSTER")
                else:
                    self.winner_text = "AI BOT WINS!"
        else:
            self.is_new_high_score = self.leaderboard_manager.update_high_score(self.score)

        self.state = State.GAME_OVER

    def set_skin(self, skin_key):
        """Updates P1 snake skin preference."""
        self.selected_skin = skin_key
        self.snake.set_skin(skin_key)

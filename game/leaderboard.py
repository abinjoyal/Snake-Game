import os
import json
from datetime import datetime
from settings import HIGHSCORE_FILE, LEADERBOARD_FILE

class LeaderboardManager:
    """
    Handles persistence of high scores and top leaderboard records using JSON.
    Includes robust exception handling for missing or corrupted files.
    """
    def __init__(self):
        self.high_score = self._load_high_score()
        self.scores_list = self._load_leaderboard()

    def _load_high_score(self):
        """Loads high score from JSON file."""
        if not os.path.exists(HIGHSCORE_FILE):
            return 0
        try:
            with open(HIGHSCORE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return int(data.get("high_score", 0))
        except (json.JSONDecodeError, ValueError, OSError) as e:
            print(f"[LeaderboardManager] Error reading high score file: {e}")
            return 0

    def _save_high_score(self):
        """Saves current high score to JSON file."""
        try:
            with open(HIGHSCORE_FILE, 'w', encoding='utf-8') as f:
                json.dump({"high_score": self.high_score}, f, indent=4)
        except OSError as e:
            print(f"[LeaderboardManager] Error writing high score file: {e}")

    def _load_leaderboard(self):
        """Loads top scores list from JSON file."""
        if not os.path.exists(LEADERBOARD_FILE):
            return []
        try:
            with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except (json.JSONDecodeError, ValueError, OSError) as e:
            print(f"[LeaderboardManager] Error reading leaderboard file: {e}")
            return []

    def _save_leaderboard(self):
        """Saves leaderboard list to JSON file."""
        try:
            with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.scores_list, f, indent=4)
        except OSError as e:
            print(f"[LeaderboardManager] Error writing leaderboard file: {e}")

    def get_high_score(self):
        """Returns highest score recorded."""
        return self.high_score

    def update_high_score(self, score):
        """
        Updates high score if current score exceeds previous record.
        Returns True if a new high score was set.
        """
        if score > self.high_score:
            self.high_score = score
            self._save_high_score()
            return True
        return False

    def get_top_scores(self, limit=10):
        """Returns top N scores sorted descending by score."""
        sorted_scores = sorted(self.scores_list, key=lambda x: x.get("score", 0), reverse=True)
        return sorted_scores[:limit]

    def add_score(self, player_name, score):
        """
        Adds a new score record with player name and formatted timestamp,
        sorts descending, trims to top 10, and persists to JSON.
        """
        clean_name = player_name.strip() if player_name.strip() else "Anonymous"
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        entry = {
            "name": clean_name[:12],  # Cap name length at 12 characters
            "score": int(score),
            "date": date_str
        }

        self.scores_list.append(entry)
        self.scores_list = sorted(self.scores_list, key=lambda x: x.get("score", 0), reverse=True)[:10]
        self._save_leaderboard()
        self.update_high_score(score)

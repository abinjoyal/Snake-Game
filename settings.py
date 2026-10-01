import os

# Window & Display Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 25
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE   # 32 tiles wide
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE # 24 tiles high
FPS = 60
DEFAULT_SPEED = 8  # Comfortable default speed (8 moves per second)

# Color Palette (Modern Dark Theme)
BG_COLOR = (15, 23, 42)          # Deep Navy Slate (#0f172a)
BG_DARK = (10, 15, 30)           # Darker backdrop
GRID_LINE_COLOR = (30, 41, 59)   # Subtle tile borders (#1e293b)
PANEL_BG = (30, 41, 59)          # Card background
TEXT_PRIMARY = (248, 250, 252)   # Soft White (#f8fafc)
TEXT_MUTED = (148, 163, 184)     # Slate Gray (#94a3b8)

# Accent Colors
ACCENT_GREEN = (16, 185, 129)    # Emerald (#10b981)
ACCENT_GREEN_HOVER = (52, 211, 153)
ACCENT_BLUE = (14, 165, 233)     # Cyan Sky (#0ea5e9)
ACCENT_RED = (239, 68, 68)       # Crimson Red (#ef4444)
ACCENT_GOLD = (245, 158, 11)     # Gold (#f59e0b)
ACCENT_PURPLE = (168, 85, 247)   # Purple (#a855f7)
ACCENT_CYAN = (6, 182, 212)      # Cyan (#06b6d4)

# Food Types & Config
FOOD_TYPES = {
    "NORMAL": {
        "name": "Apple",
        "color": (239, 68, 68),
        "points": 10,
        "grow": 1,
        "chance": 0.50
    },
    "GOLDEN": {
        "name": "Golden Star",
        "color": (245, 158, 11),
        "points": 30,
        "grow": 2,
        "chance": 0.10,
        "lifetime": 360  # Frames before despawn (6 seconds)
    },
    "SPEED_BOOST": {
        "name": "Speed Lightning",
        "color": (14, 165, 233),
        "points": 15,
        "grow": 1,
        "chance": 0.08,
        "lifetime": 300
    },
    "SLOW_MO": {
        "name": "Slow Turtle",
        "color": (6, 182, 212),
        "points": 15,
        "grow": 1,
        "chance": 0.08,
        "lifetime": 300
    },
    "SHRINK": {
        "name": "Shrink Berry",
        "color": (168, 85, 247),
        "points": 10,
        "grow": -2,
        "chance": 0.08,
        "lifetime": 300
    },
    "MAGNET": {
        "name": "Food Magnet",
        "color": (234, 179, 8),   # Vibrant Amber (#eab308)
        "points": 15,
        "grow": 1,
        "chance": 0.08,
        "lifetime": 300
    },
    "SHIELD": {
        "name": "Shield Bubble",
        "color": (56, 189, 248),   # Sky Cyan (#38bdf8)
        "points": 15,
        "grow": 1,
        "chance": 0.08,
        "lifetime": 300
    }
}

# Map Modes
MAP_MODES = {
    "CLASSIC": "Classic Walls",
    "PORTAL": "Portal Teleport",
    "OBSTACLES": "Maze Obstacles",
    "CAMPAIGN": "Campaign Mode",
    "CUSTOM": "Custom Map"
}

# Pre-designed Obstacle Walls (Grid Coordinates) for Maze Mode
MAZE_OBSTACLES = set([
    # Top-Left Block
    (7, 6), (8, 6), (9, 6), (7, 7),
    # Top-Right Block
    (22, 6), (23, 6), (24, 6), (24, 7),
    # Bottom-Left Block
    (7, 17), (7, 18), (8, 18), (9, 18),
    # Bottom-Right Block
    (24, 17), (22, 18), (23, 18), (24, 18),
    # Center Pillars
    (15, 11), (16, 11), (15, 12), (16, 12)
])

# Snake Skins Configuration
SKINS = {
    "classic": {
        "name": "Classic Emerald",
        "description": "The timeless green snake with vibrant head.",
        "head": (16, 185, 129),
        "body_start": (52, 211, 153),
        "body_end": (4, 120, 87),
        "eye_color": (255, 255, 255)
    },
    "blue": {
        "name": "Cyber Blue",
        "description": "Futuristic neon blue gradient skin.",
        "head": (14, 165, 233),
        "body_start": (56, 189, 248),
        "body_end": (3, 105, 161),
        "eye_color": (255, 255, 255)
    },
    "neon": {
        "name": "Neon Glow",
        "description": "Electric pink and glowing magenta.",
        "head": (236, 72, 153),
        "body_start": (244, 114, 182),
        "body_end": (190, 24, 93),
        "eye_color": (255, 255, 255)
    },
    "fire": {
        "name": "Inferno Fire",
        "description": "Fiery crimson and burning orange.",
        "head": (239, 68, 68),
        "body_start": (249, 115, 22),
        "body_end": (185, 28, 28),
        "eye_color": (255, 230, 0)
    },
    "rainbow": {
        "name": "Rainbow Shift",
        "description": "Dynamic multi-color spectrum shift.",
        "head": (255, 255, 255),
        "body_start": (255, 0, 0),
        "body_end": (0, 0, 255),
        "eye_color": (15, 23, 42)
    }
}

# File System Directories & Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

HIGHSCORE_FILE = os.path.join(DATA_DIR, "highscore.json")
LEADERBOARD_FILE = os.path.join(DATA_DIR, "leaderboard.json")
ACHIEVEMENTS_FILE = os.path.join(DATA_DIR, "achievements.json")
CUSTOM_MAP_FILE = os.path.join(DATA_DIR, "custom_map.json")

# Ensure required directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SOUNDS_DIR, exist_ok=True)

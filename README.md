# Classic Snake Game

A modern, feature-packed, and responsive **Classic & Power-Up Snake Game** built in Python with **Pygame**. Designed with sleek dark UI styling, responsive controls, procedural sound synthesis, particle explosion graphics, 2-Player local co-op/versus, AI Bot Opponents, interactive Map Builder, unlockable Achievements, multi-map boundary modes, synthesized retro BGM, and persistent JSON leaderboards.

---

## Key Features

- **3 Game Modes**:
  - **1-Player Solo**: Classic high score hunt.
  - **2-Player Local Versus**: Play side-by-side on the same keyboard (`WASD` vs `Arrow Keys`).
  - **Player vs AI Bot**: Race against a pathfinding AI Bot snake for food!

- **5 Map Modes**:
  - **Classic**: Traditional wall boundaries cause game over.
  - **Portal Teleport**: Teleport across screen edges (Torus mode).
  - **Maze Obstacles**: Navigate around fixed brick obstacle layouts.
  - **Campaign Mode**: Levels advance every 100 points, increasing speed dynamically.
  - **Custom Map**: Play on brick obstacle layouts built with the in-game Map Builder!

- **7 Special Foods & Power-Ups**:
  - **Normal Red Apple**: +10 pts, normal growth.
  - **Golden Star (30 pts)**: Timed bonus food with sparkling gold effects.
  - **Speed Lightning (Blue)**: 1.5x speed boost for 5 seconds.
  - **Slow Turtle (Cyan)**: 0.7x slow-motion control for 5 seconds.
  - **Shrink Berry (Purple)**: Reduces snake body length by 2 segments.
  - **Food Magnet (Amber)**: Pulls nearby food towards snake head automatically.
  - **Shield Bubble (Cyan)**: Protects against 1 fatal wall or self-collision!

- **Achievement & Trophy System**:
  - Unlocks 8 unique badges (*First Bite, Combo Master, Life Saver, Centurion, Bot Buster, etc.*) with animated in-game toast notifications.

- **Interactive Map Builder**:
  - Grid editor screen allowing players to paint and erase brick obstacle walls and save them (`data/custom_map.json`).

- **Synthesized Audio & Retro BGM**:
  - Zero-dependency procedural 8-bit sound synth for chiptune background music and sound effects (eat, click, pause, gameover, powerup, combo, shield, fanfare).

---

## Technologies Used

- **Language**: Python 3.8+
- **Game Engine**: Pygame 2.5+
- **Persistence**: JSON (`highscore.json`, `leaderboard.json`, `achievements.json`, `custom_map.json`)
- **Audio & Visuals**: Wave sound synthesis & Pygame Alpha Particle Engine
- **AI Algorithm**: A* Pathfinding with Safety Heuristics
- **Architecture**: Modular Object-Oriented Programming (OOP)

---

## Project Structure

```text
snake-game/
│
├── main.py                     # Entry point & main game loop with camera shake & particles
├── settings.py                 # Colors, screen size, FPS, food definitions, map paths
│
├── game/
│   ├── snake.py                # Snake logic, direction queue, shrink, shield & skin rendering
│   ├── ai_snake.py             # A* pathfinding AI Bot opponent controller
│   ├── food.py                 # Multi-food variant generator & pulse animations
│   ├── collision.py            # Boundary, obstacle, self, & snake-vs-snake collision
│   ├── game_state.py           # Finite State Machine, combo manager, campaign levels
│   ├── achievements.py         # Achievement manager, JSON storage & toast notifications
│   ├── leaderboard.py          # JSON leaderboard & high score manager
│   ├── particle.py             # Particle burst physics & screen shake manager
│   └── sound_manager.py        # Procedural audio synthesizer & chiptune BGM generator
│
├── ui/
│   ├── components.py           # Reusable widgets: Button, TextInput, Cards
│   ├── menu.py                 # Main Menu with 1P/2P/VS_AI & Map selectors
│   ├── game_over.py            # Game Over modal screen with winner banners
│   ├── leaderboard_screen.py   # Top 10 Hall of Fame table UI
│   ├── achievements_screen.py  # Trophy gallery screen
│   ├── map_builder_screen.py   # Interactive grid obstacle editor
│   ├── skins_screen.py         # Skin selection gallery & live animated preview
│   └── settings_screen.py      # Audio/BGM toggles, Map modes, & game speed options
│
├── assets/
│   └── sounds/                 # Auto-generated sound effect WAV files & BGM loop
│
├── data/
│   ├── highscore.json          # Persisted best high score
│   ├── leaderboard.json        # Persisted top 10 scores
│   ├── achievements.json       # Persisted unlocked trophies
│   └── custom_map.json         # User-designed custom map layout
│
├── requirements.txt            # Project dependencies
└── README.md                   # Documentation
```

---

## Installation & Running

### 1. Install Dependencies
Make sure you have Python 3 installed. Run in your terminal:

```bash
pip install -r requirements.txt
```

### 2. Run the Game
Execute `main.py`:

```bash
python main.py
```

---

## Controls Guide

| Action | Player 1 / Solo | Player 2 (2P Mode) | Map Builder |
| :--- | :--- | :--- | :--- |
| **Move Up** | `W` (or `Up Arrow`) | `Up Arrow` | — |
| **Move Down** | `S` (or `Down Arrow`) | `Down Arrow` | — |
| **Move Left** | `A` (or `Left Arrow`) | `Left Arrow` | — |
| **Move Right** | `D` (or `Right Arrow`) | `Right Arrow` | — |
| **Paint Wall** | — | — | `Left Click` |
| **Erase Wall** | — | — | `Right Click` |
| **Pause / Resume** | `P` / `ESC` | `P` / `ESC` | — |
| **Quick Restart** | `R` | `R` | — |

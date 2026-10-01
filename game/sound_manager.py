import os
import math
import wave
import struct
import pygame
from settings import SOUNDS_DIR

class SoundManager:
    """
    Manages game sound effects and audio settings.
    Procedurally generates sample WAV sounds if audio files are missing.
    """
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        
        # Initialize pygame mixer safely
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        except Exception as e:
            print(f"[SoundManager] Warning: Audio mixer initialization failed: {e}")
            self.enabled = False
            return
            
        self._ensure_sound_files()
        self._load_sounds()
        self.bgm_enabled = True
        self.bgm_playing = False

    def _ensure_sound_files(self):
        """Generates 8-bit synthetic wave audio files if not present on disk."""
        files_to_generate = {
            "eat.wav": self._generate_eat_wav,
            "click.wav": self._generate_click_wav,
            "gameover.wav": self._generate_gameover_wav,
            "pause.wav": self._generate_pause_wav,
            "powerup.wav": self._generate_powerup_wav,
            "combo.wav": self._generate_combo_wav,
            "shield.wav": self._generate_shield_wav,
            "achievement.wav": self._generate_achievement_wav,
            "bgm.wav": self._generate_bgm_wav
        }

        for filename, generator in files_to_generate.items():
            path = os.path.join(SOUNDS_DIR, filename)
            if not os.path.exists(path):
                try:
                    generator(path)
                except Exception as e:
                    print(f"[SoundManager] Could not generate sound file {filename}: {e}")

    def _generate_eat_wav(self, file_path):
        """Synthesizes a short ascending double chime sound."""
        sample_rate = 22050
        duration = 0.12
        num_samples = int(sample_rate * duration)
        
        with wave.open(file_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for i in range(num_samples):
                t = float(i) / sample_rate
                freq = 600 + (t / duration) * 600
                amplitude = 12000 * (1.0 - t / duration)
                val = int(amplitude * math.sin(2.0 * math.pi * freq * t))
                data = struct.pack('<h', val)
                wav_file.writeframesraw(data)

    def _generate_click_wav(self, file_path):
        """Synthesizes a clean button click sound."""
        sample_rate = 22050
        duration = 0.05
        num_samples = int(sample_rate * duration)
        
        with wave.open(file_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for i in range(num_samples):
                t = float(i) / sample_rate
                freq = 800
                amplitude = 10000 * (1.0 - t / duration)
                val = int(amplitude * math.sin(2.0 * math.pi * freq * t))
                data = struct.pack('<h', val)
                wav_file.writeframesraw(data)

    def _generate_gameover_wav(self, file_path):
        """Synthesizes a descending game over sound effect."""
        sample_rate = 22050
        duration = 0.4
        num_samples = int(sample_rate * duration)
        
        with wave.open(file_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for i in range(num_samples):
                t = float(i) / sample_rate
                freq = max(100.0, 500.0 - (t / duration) * 400.0)
                amplitude = 14000 * (1.0 - t / duration)
                val = int(amplitude * math.sin(2.0 * math.pi * freq * t))
                data = struct.pack('<h', val)
                wav_file.writeframesraw(data)

    def _generate_pause_wav(self, file_path):
        """Synthesizes a soft pause tone sound."""
        sample_rate = 22050
        duration = 0.08
        num_samples = int(sample_rate * duration)
        
        with wave.open(file_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for i in range(num_samples):
                t = float(i) / sample_rate
                freq = 550
                amplitude = 9000 * (1.0 - t / duration)
                val = int(amplitude * math.sin(2.0 * math.pi * freq * t))
                data = struct.pack('<h', val)
                wav_file.writeframesraw(data)

    def _generate_powerup_wav(self, file_path):
        """Synthesizes a high-pitched powerup chime."""
        sample_rate = 22050
        duration = 0.2
        num_samples = int(sample_rate * duration)
        
        with wave.open(file_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for i in range(num_samples):
                t = float(i) / sample_rate
                freq = 800 + (t / duration) * 800
                amplitude = 14000 * (1.0 - t / duration)
                val = int(amplitude * math.sin(2.0 * math.pi * freq * t))
                data = struct.pack('<h', val)
                wav_file.writeframesraw(data)

    def _generate_combo_wav(self, file_path):
        """Synthesizes an energetic combo synth chime."""
        sample_rate = 22050
        duration = 0.15
        num_samples = int(sample_rate * duration)
        
        with wave.open(file_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for i in range(num_samples):
                t = float(i) / sample_rate
                freq = 1000 + math.sin(t * 50) * 300
                amplitude = 13000 * (1.0 - t / duration)
                val = int(amplitude * math.sin(2.0 * math.pi * freq * t))
                data = struct.pack('<h', val)
                wav_file.writeframesraw(data)

    def _generate_shield_wav(self, file_path):
        """Synthesizes a glassy shield energy absorption wave."""
        sample_rate = 22050
        duration = 0.25
        num_samples = int(sample_rate * duration)
        
        with wave.open(file_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for i in range(num_samples):
                t = float(i) / sample_rate
                freq = 1200 - (t / duration) * 700
                amplitude = 15000 * math.sin(math.pi * (t / duration))
                val = int(amplitude * math.sin(2.0 * math.pi * freq * t))
                data = struct.pack('<h', val)
                wav_file.writeframesraw(data)

    def _generate_achievement_wav(self, file_path):
        """Synthesizes a triumphant 3-note fanfare flourish."""
        sample_rate = 22050
        duration = 0.35
        num_samples = int(sample_rate * duration)
        
        with wave.open(file_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            notes = [523.25, 659.25, 783.99] # C5, E5, G5
            note_len = duration / 3.0
            
            for i in range(num_samples):
                t = float(i) / sample_rate
                note_idx = min(2, int(t / note_len))
                freq = notes[note_idx]
                amplitude = 12000 * (1.0 - (t % note_len) / note_len)
                val = int(amplitude * math.sin(2.0 * math.pi * freq * t))
                data = struct.pack('<h', val)
                wav_file.writeframesraw(data)

    def _generate_bgm_wav(self, file_path):
        """Synthesizes a retro 8-bit chiptune background music loop (2 seconds)."""
        sample_rate = 22050
        duration = 2.0
        num_samples = int(sample_rate * duration)
        
        # Arpeggiated melody frequencies (Pentatonic synth loop)
        sequence = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 261.63, 196.00]
        step_len = duration / len(sequence)

        with wave.open(file_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for i in range(num_samples):
                t = float(i) / sample_rate
                step_idx = int((t / duration) * len(sequence)) % len(sequence)
                freq = sequence[step_idx]
                # Square wave effect for 8-bit retro feel
                sq_val = 1.0 if math.sin(2.0 * math.pi * freq * t) > 0 else -1.0
                amplitude = 3000 * (0.5 + 0.5 * math.sin(t * 10))
                val = int(amplitude * sq_val)
                data = struct.pack('<h', val)
                wav_file.writeframesraw(data)

    def _load_sounds(self):
        """Loads WAV files into Pygame sound objects."""
        sound_keys = ["eat", "click", "gameover", "pause", "powerup", "combo", "shield", "achievement", "bgm"]
        for key in sound_keys:
            path = os.path.join(SOUNDS_DIR, f"{key}.wav")
            if os.path.exists(path):
                try:
                    self.sounds[key] = pygame.mixer.Sound(path)
                except Exception as e:
                    print(f"[SoundManager] Error loading sound {key}: {e}")

    def play(self, sound_name):
        """Plays the specified sound effect if sound is enabled."""
        if not self.enabled:
            return
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"[SoundManager] Play exception: {e}")

    def play_eat(self):
        self.play("eat")

    def play_click(self):
        self.play("click")

    def play_gameover(self):
        self.stop_bgm()
        self.play("gameover")

    def play_pause(self):
        self.play("pause")

    def play_powerup(self):
        self.play("powerup")

    def play_combo(self):
        self.play("combo")

    def play_shield_pop(self):
        self.play("shield")

    def play_achievement(self):
        self.play("achievement")

    def start_bgm(self):
        """Starts looping retro background music."""
        if self.enabled and self.bgm_enabled and "bgm" in self.sounds:
            try:
                self.sounds["bgm"].play(loops=-1)
                self.bgm_playing = True
            except Exception as e:
                print(f"[SoundManager] BGM start exception: {e}")

    def stop_bgm(self):
        """Stops background music playback."""
        if "bgm" in self.sounds:
            try:
                self.sounds["bgm"].stop()
                self.bgm_playing = False
            except Exception as e:
                pass

    def toggle_sound(self):
        """Toggles sound effects ON/OFF."""
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop_bgm()
        return self.enabled

    def toggle_bgm(self):
        """Toggles background music ON/OFF."""
        self.bgm_enabled = not self.bgm_enabled
        if not self.bgm_enabled:
            self.stop_bgm()
        return self.bgm_enabled

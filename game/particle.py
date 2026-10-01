import random
import math
import pygame

class Particle:
    """Represents a single visual particle effect (sparkle, explosion fragment)."""
    def __init__(self, x, y, color, vx=None, vy=None, radius=None, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1.5, 4.5)
        self.vx = vx if vx is not None else math.cos(angle) * speed
        self.vy = vy if vy is not None else math.sin(angle) * speed
        self.radius = radius if radius is not None else random.uniform(2.5, 5.0)
        self.max_lifetime = lifetime
        self.lifetime = lifetime

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.94  # Friction / damping
        self.vy *= 0.94
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime <= 0:
            return
        alpha = int((self.lifetime / self.max_lifetime) * 255)
        current_radius = max(1, int(self.radius * (self.lifetime / self.max_lifetime)))
        
        # Transparent particle surface
        s = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)
        color_with_alpha = (*self.color[:3], alpha)
        pygame.draw.circle(s, color_with_alpha, (current_radius, current_radius), current_radius)
        surface.blit(s, (int(self.x) - current_radius, int(self.y) - current_radius))

class ParticleManager:
    """Manages collections of particles and screen shake camera offsets."""
    def __init__(self):
        self.particles = []
        self.shake_amount = 0
        self.shake_offset = (0, 0)

    def add_burst(self, x, y, color, count=16):
        """Spawns an explosive particle burst at pixel coordinates (x, y)."""
        for _ in range(count):
            self.particles.append(Particle(x, y, color, lifetime=random.randint(20, 35)))

    def add_gold_sparkles(self, x, y, count=8):
        """Spawns floating golden sparkle particles."""
        gold_colors = [(245, 158, 11), (251, 191, 36), (254, 240, 138), (255, 255, 255)]
        for _ in range(count):
            c = random.choice(gold_colors)
            self.particles.append(Particle(x, y, c, lifetime=random.randint(25, 45)))

    def trigger_screen_shake(self, intensity=10):
        """Triggers screen shake intensity on high-impact events like game over."""
        self.shake_amount = intensity

    def update(self):
        """Updates particle positions and screen shake offsets."""
        # Update particles
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for p in self.particles:
            p.update()

        # Update screen shake
        if self.shake_amount > 0:
            self.shake_offset = (
                random.randint(-self.shake_amount, self.shake_amount),
                random.randint(-self.shake_amount, self.shake_amount)
            )
            self.shake_amount -= 1
        else:
            self.shake_offset = (0, 0)

    def draw(self, surface):
        """Renders active particles."""
        for p in self.particles:
            p.draw(surface)

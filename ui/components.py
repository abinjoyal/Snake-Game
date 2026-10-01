import pygame
from settings import (
    TEXT_PRIMARY, TEXT_MUTED, PANEL_BG, ACCENT_GREEN,
    ACCENT_GREEN_HOVER, BG_DARK
)

def draw_text(surface, text, font, color, center_pos, shadow=True):
    """
    Renders text centered at center_pos with an optional drop shadow.
    """
    if shadow:
        shadow_surface = font.render(text, True, (10, 15, 30))
        shadow_rect = shadow_surface.get_rect(center=(center_pos[0] + 2, center_pos[1] + 2))
        surface.blit(shadow_surface, shadow_rect)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center_pos)
    surface.blit(text_surface, text_rect)
    return text_rect

def draw_text_glow(surface, text, font, color, glow_color, center_pos):
    """
    Renders text with a subtle dual-pass glowing halo effect.
    """
    glow_surface = font.render(text, True, glow_color)
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1)]:
        glow_rect = glow_surface.get_rect(center=(center_pos[0] + dx, center_pos[1] + dy))
        surface.blit(glow_surface, glow_rect)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center_pos)
    surface.blit(text_surface, text_rect)
    return text_rect

class Button:
    """
    Interactive UI button widget supporting hover animations,
    click callbacks, rounded borders, and sound effects.
    """
    def __init__(self, rect, text, callback, font,
                 bg_color=PANEL_BG, hover_color=ACCENT_GREEN,
                 text_color=TEXT_PRIMARY, border_color=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.is_hovered = False

    def handle_event(self, event, sound_manager=None):
        """Processes mouse movement and click events."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if sound_manager:
                    sound_manager.play_click()
                if self.callback:
                    self.callback()
                return True
        return False

    def draw(self, surface):
        """Renders button with hover highlights and smooth styling."""
        color = self.hover_color if self.is_hovered else self.bg_color
        
        # Shadow effect
        shadow_rect = self.rect.copy()
        shadow_rect.y += 3
        pygame.draw.rect(surface, (10, 15, 30), shadow_rect, border_radius=10)

        # Button Body
        pygame.draw.rect(surface, color, self.rect, border_radius=10)

        # Glow Border when hovered
        outline_color = self.border_color or (self.hover_color if self.is_hovered else (50, 65, 85))
        border_width = 2 if self.is_hovered else 1
        pygame.draw.rect(surface, outline_color, self.rect, width=border_width, border_radius=10)

        # Display Label Text
        draw_text(surface, self.text, self.font, self.text_color, self.rect.center, shadow=True)

class TextInput:
    """
    Interactive text input field for player name entry.
    Supports typing, backspace, character limit, and blinking cursor.
    """
    def __init__(self, rect, font, max_length=12, initial_text=""):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.max_length = max_length
        self.text = initial_text
        self.active = True
        self.cursor_timer = 0

    def handle_event(self, event):
        """Handles keyboard input events."""
        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return True
            else:
                if len(self.text) < self.max_length and event.unicode.isprintable():
                    self.text += event.unicode
        return False

    def update(self):
        """Updates cursor blink timer."""
        self.cursor_timer = (self.cursor_timer + 1) % 60

    def draw(self, surface):
        """Renders input field box and text with blinking cursor."""
        pygame.draw.rect(surface, BG_DARK, self.rect, border_radius=8)
        
        border_color = ACCENT_GREEN if self.active else (60, 80, 100)
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=8)

        display_text = self.text if self.text else "Enter Name..."
        text_color = TEXT_PRIMARY if self.text else TEXT_MUTED
        
        text_surface = self.font.render(display_text, True, text_color)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 15, self.rect.centery))
        surface.blit(text_surface, text_rect)

        if self.active and self.cursor_timer < 30:
            cursor_x = text_rect.right + 4 if self.text else self.rect.x + 15
            pygame.draw.line(surface, TEXT_PRIMARY,
                             (cursor_x, self.rect.centery - 10),
                             (cursor_x, self.rect.centery + 10), 2)

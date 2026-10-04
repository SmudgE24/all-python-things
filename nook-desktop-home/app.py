import math
import os
import sys
from datetime import datetime

import pygame

# -----------------------------------------------------------------------------
# Mac-inspired desktop homepage for Pygame.
# Plugins are intentionally self-contained in this file so the app is portable.
# -----------------------------------------------------------------------------

WIDTH, HEIGHT = 1280, 800
FPS = 60
BG = (14, 18, 28)
PANEL = (22, 28, 42)
PANEL_2 = (28, 35, 52)
BORDER = (47, 58, 82)
TEXT = (238, 242, 249)
MUTED = (151, 163, 187)
ACCENT = (111, 137, 255)
ACCENT_2 = (94, 220, 192)
WARNING = (255, 190, 91)
DANGER = (255, 112, 124)


def clamp(value, low, high):
    return max(low, min(high, value))


class Plugin:
    """Base type for small, self-contained dashboard plugins."""

    key = "plugin"
    name = "Plugin"
    icon = "?"
    description = ""
    color = ACCENT

    def __init__(self):
        self.app = None

    def attach(self, app):
        self.app = app

    def draw(self, surface, rect, font, small_font):
        pass

    def handle_event(self, event):
        pass


class FocusPlugin(Plugin):
    key, name, icon = "focus", "Focus", "◷"
    description = "A small timer for deep work"
    color = (128, 149, 255)

    def __init__(self):
        super().__init__()
        self.remaining = 25 * 60
        self.running = False
        self.last_tick = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if self.running:
            self.remaining -= (now - self.last_tick) / 1000
            if self.remaining <= 0:
                self.remaining = 25 * 60
                self.running = False
        self.last_tick = now

    def draw(self, surface, rect, font, small_font):
        self.update()
        mins, secs = divmod(max(0, int(self.remaining)), 60)
        title = font.render("Focus timer", True, TEXT)
        surface.blit(title, (rect.x + 22, rect.y + 18))
        state = "IN SESSION" if self.running else "READY WHEN YOU ARE"
        surface.blit(small_font.render(state, True, ACCENT_2 if self.running else MUTED), (rect.x + 22, rect.y + 52))
        time_text = font.render(f"{mins:02d}:{secs:02d}", True, TEXT)
        surface.blit(time_text, time_text.get_rect(center=(rect.centerx, rect.y + 122)))
        pygame.draw.rect(surface, BORDER, (rect.x + 22, rect.y + 150, rect.w - 44, 6), border_radius=3)
        progress = 1 - self.remaining / (25 * 60)
        pygame.draw.rect(surface, ACCENT, (rect.x + 22, rect.y + 150, int((rect.w - 44) * progress), 6), border_radius=3)
        button = pygame.Rect(rect.centerx - 58, rect.bottom - 52, 116, 32)
        pygame.draw.rect(surface, ACCENT if not self.running else PANEL_2, button, border_radius=8)
        if self.running:
            pygame.draw.rect(surface, ACCENT, button, 1, border_radius=8)
        label = "Pause" if self.running else "Start focus"
        surface.blit(small_font.render(label, True, TEXT), small_font.render(label, True, TEXT).get_rect(center=button.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.running = not self.running


class NotesPlugin(Plugin):
    key, name, icon = "notes", "Quick note", "✎"
    description = "Capture a thought without leaving home"
    color = (244, 183, 90)

    def __init__(self):
        super().__init__()
        self.text = "Ship the first version"
        self.active = False

    def draw(self, surface, rect, font, small_font):
        surface.blit(font.render("Quick note", True, TEXT), (rect.x + 22, rect.y + 18))
        surface.blit(small_font.render("A scratchpad for today", True, MUTED), (rect.x + 22, rect.y + 52))
        box = pygame.Rect(rect.x + 22, rect.y + 82, rect.w - 44, 78)
        pygame.draw.rect(surface, (18, 23, 35), box, border_radius=8)
        pygame.draw.rect(surface, ACCENT if self.active else BORDER, box, 1, border_radius=8)
        note = self.text or "Start typing..."
        surface.blit(small_font.render(note[:34], True, TEXT if self.text else MUTED), (box.x + 12, box.y + 14))
        if self.active and (pygame.time.get_ticks() // 500) % 2 == 0:
            width = small_font.size(note[:34])[0]
            pygame.draw.line(surface, ACCENT, (box.x + 12 + width, box.y + 12), (box.x + 12 + width, box.y + 34), 2)
        hint = "Click to edit · Enter to save"
        surface.blit(small_font.render(hint, True, MUTED), (rect.x + 22, rect.bottom - 30))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.active = True
            pygame.key.start_text_input()
        elif event.type == pygame.TEXTINPUT and self.active:
            self.text += event.text
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.active = False
                pygame.key.stop_text_input()


class WeatherPlugin(Plugin):
    key, name, icon = "weather", "Weather", "☼"
    description = "A glance at the outside world"
    color = (94, 220, 192)

    def draw(self, surface, rect, font, small_font):
        surface.blit(font.render("Weather", True, TEXT), (rect.x + 22, rect.y + 18))
        surface.blit(small_font.render("Cupertino · Updated just now", True, MUTED), (rect.x + 22, rect.y + 52))
        surface.blit(font.render("☼", True, WARNING), (rect.x + 28, rect.y + 94))
        surface.blit(font.render("21°", True, TEXT), (rect.x + 94, rect.y + 100))
        surface.blit(small_font.render("Clear skies", True, ACCENT_2), (rect.x + 96, rect.y + 137))
        for i, (day, temp) in enumerate((("Today", "21°"), ("Wed", "19°"), ("Thu", "22°"))):
            x = rect.right - 165 + i * 48
            surface.blit(small_font.render(day, True, MUTED), (x, rect.y + 101))
            surface.blit(small_font.render(temp, True, TEXT), (x, rect.y + 127))


class CalculatorPlugin(Plugin):
    key, name, icon = "calc", "Calculator", "＋"
    description = "Fast arithmetic, always close at hand"
    color = (218, 133, 255)

    def __init__(self):
        super().__init__()
        self.display = "42"

    def draw(self, surface, rect, font, small_font):
        surface.blit(font.render("Calculator", True, TEXT), (rect.x + 22, rect.y + 18))
        display = pygame.Rect(rect.x + 22, rect.y + 72, rect.w - 44, 54)
        pygame.draw.rect(surface, (18, 23, 35), display, border_radius=8)
        pygame.draw.rect(surface, BORDER, display, 1, border_radius=8)
        value = font.render(self.display, True, TEXT)
        surface.blit(value, (display.right - value.get_width() - 12, display.y + 11))
        keys = ["7", "8", "9", "÷", "4", "5", "6", "×", "1", "2", "3", "−"]
        for i, key in enumerate(keys):
            x = rect.x + 22 + (i % 4) * 45
            y = rect.y + 140 + (i // 4) * 30
            surface.blit(small_font.render(key, True, ACCENT if key in "÷×−" else MUTED), (x, y))
        surface.blit(small_font.render("Click keys coming next", True, MUTED), (rect.x + 22, rect.bottom - 30))


# The complete plugin catalog lives in this file by design.
PLUGIN_CLASSES = [FocusPlugin, NotesPlugin, WeatherPlugin, CalculatorPlugin]


class DashboardApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Nook — Desktop Home")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Avenir Next", 22)
        self.title_font = pygame.font.SysFont("Avenir Next", 34, bold=True)
        self.big_font = pygame.font.SysFont("Avenir Next", 48, bold=True)
        self.small_font = pygame.font.SysFont("Avenir Next", 14)
        self.tiny_font = pygame.font.SysFont("Avenir Next", 12)
        self.running = True
        self.active_view = "home"
        self.plugins = [cls() for cls in PLUGIN_CLASSES]
        for plugin in self.plugins:
            plugin.attach(self)
        self.toast = ""
        self.toast_until = 0

    def notify(self, message):
        self.toast = message
        self.toast_until = pygame.time.get_ticks() + 2200

    def rounded_panel(self, rect, color=PANEL, outline=BORDER):
        pygame.draw.rect(self.screen, color, rect, border_radius=14)
        pygame.draw.rect(self.screen, outline, rect, 1, border_radius=14)

    def draw_sidebar(self):
        sidebar = pygame.Rect(0, 0, 230, self.screen.get_height())
        pygame.draw.rect(self.screen, (18, 23, 35), sidebar)
        pygame.draw.line(self.screen, BORDER, (sidebar.right, 0), (sidebar.right, sidebar.bottom), 1)
        brand = self.title_font.render("nook", True, TEXT)
        self.screen.blit(brand, (28, 28))
        self.screen.blit(self.small_font.render("your calm command center", True, MUTED), (29, 70))
        items = [("home", "⌂", "Overview"), ("plugins", "◈", "All plugins")]
        y = 132
        for key, icon, label in items:
            row = pygame.Rect(16, y, 198, 42)
            if self.active_view == key:
                pygame.draw.rect(self.screen, (37, 48, 74), row, border_radius=9)
            self.screen.blit(self.font.render(icon, True, ACCENT if self.active_view == key else MUTED), (30, y + 8))
            self.screen.blit(self.small_font.render(label, True, TEXT if self.active_view == key else MUTED), (67, y + 13))
            y += 50
        self.screen.blit(self.small_font.render("YOUR PLUGINS", True, MUTED), (28, 256))
        y = 284
        for plugin in self.plugins:
            self.screen.blit(self.font.render(plugin.icon, True, plugin.color), (29, y))
            self.screen.blit(self.small_font.render(plugin.name, True, TEXT), (67, y + 6))
            y += 42
        pygame.draw.line(self.screen, BORDER, (28, self.screen.get_height() - 80), (202, self.screen.get_height() - 80), 1)
        self.screen.blit(self.small_font.render("⌘  +  K", True, TEXT), (28, self.screen.get_height() - 58))
        self.screen.blit(self.tiny_font.render("Open command palette", True, MUTED), (102, self.screen.get_height() - 56))

    def draw_home(self):
        w, h = self.screen.get_size()
        content = pygame.Rect(230, 0, w - 230, h)
        self.screen.fill(BG, content)
        now = datetime.now()
        self.screen.blit(self.small_font.render(now.strftime("%A, %B %-d"), True, MUTED), (content.x + 52, 42))
        self.screen.blit(self.title_font.render("Good morning, Ethan.", True, TEXT), (content.x + 50, 72))
        self.screen.blit(self.small_font.render("Here’s a clear place to start your day.", True, MUTED), (content.x + 52, 120))
        status = pygame.Rect(w - 230 - 180, 48, 126, 32)
        pygame.draw.rect(self.screen, (26, 53, 55), status, border_radius=8)
        self.screen.blit(self.tiny_font.render("●  SYSTEM READY", True, ACCENT_2), (status.x + 13, status.y + 10))

        card_y = 180
        gap = 18
        card_w = int((content.w - 100 - gap * 2) / 3)
        cards = [
            ("TODAY", "3", "things on your list", ACCENT),
            ("STREAK", "7", "days in a row", ACCENT_2),
            ("UP NEXT", "09:30", "design review", WARNING),
        ]
        for i, (eyebrow, value, label, color) in enumerate(cards):
            rect = pygame.Rect(content.x + 50 + i * (card_w + gap), card_y, card_w, 108)
            self.rounded_panel(rect)
            self.screen.blit(self.tiny_font.render(eyebrow, True, MUTED), (rect.x + 18, rect.y + 16))
            self.screen.blit(self.big_font.render(value, True, color), (rect.x + 18, rect.y + 39))
            self.screen.blit(self.tiny_font.render(label, True, MUTED), (rect.right - 18 - self.tiny_font.size(label)[0], rect.y + 69))

        section_y = 322
        self.screen.blit(self.font.render("Your space", True, TEXT), (content.x + 50, section_y))
        self.screen.blit(self.small_font.render("Tiny tools, ready when you are.", True, MUTED), (content.x + 50, section_y + 32))
        plugin_y = section_y + 70
        plugin_h = 218
        for i, plugin in enumerate(self.plugins):
            col = i % 2
            row = i // 2
            rect = pygame.Rect(content.x + 50 + col * (card_w + gap), plugin_y + row * (plugin_h + gap), card_w, plugin_h)
            self.rounded_panel(rect)
            plugin.draw(self.screen, rect, self.font, self.small_font)

    def draw_plugins(self):
        w, h = self.screen.get_size()
        self.screen.fill(BG)
        self.screen.blit(self.title_font.render("All plugins", True, TEXT), (280, 48))
        self.screen.blit(self.small_font.render("Everything bundled with this nook, in one place.", True, MUTED), (282, 94))
        for i, plugin in enumerate(self.plugins):
            rect = pygame.Rect(280, 150 + i * 120, min(650, w - 330), 96)
            self.rounded_panel(rect)
            pygame.draw.circle(self.screen, plugin.color, (rect.x + 36, rect.centery), 20)
            self.screen.blit(self.font.render(plugin.icon, True, BG), (rect.x + 26, rect.y + 26))
            self.screen.blit(self.font.render(plugin.name, True, TEXT), (rect.x + 76, rect.y + 20))
            self.screen.blit(self.small_font.render(plugin.description, True, MUTED), (rect.x + 76, rect.y + 52))
            self.screen.blit(self.small_font.render("ACTIVE", True, ACCENT_2), (rect.right - 70, rect.y + 23))

    def draw(self):
        self.screen.fill(BG)
        self.draw_sidebar()
        if self.active_view == "home":
            self.draw_home()
        else:
            self.draw_plugins()
        if self.toast and pygame.time.get_ticks() < self.toast_until:
            toast = pygame.Rect(self.screen.get_width() - 320, self.screen.get_height() - 66, 270, 38)
            self.rounded_panel(toast, (33, 43, 64), ACCENT)
            self.screen.blit(self.small_font.render(self.toast, True, TEXT), (toast.x + 14, toast.y + 11))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.active_view = "home"
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x, y = event.pos
            if x < 230:
                if 132 <= y < 174:
                    self.active_view = "home"
                elif 182 <= y < 224:
                    self.active_view = "plugins"
                return
            # Keep cards interactive while on the home page.
            if self.active_view == "home":
                w = self.screen.get_width()
                card_w = int(((w - 230) - 100 - 36) / 3)
                plugin_y = 392
                gap = 18
                for i, plugin in enumerate(self.plugins):
                    col, row = i % 2, i // 2
                    rect = pygame.Rect(230 + 50 + col * (card_w + gap), plugin_y + row * (236), card_w, 218)
                    if rect.collidepoint(event.pos):
                        plugin.handle_event(event)
                        return
                if 132 <= y < 224:
                    self.notify("Plugins are already at home")
        elif self.active_view == "home":
            for plugin in self.plugins:
                plugin.handle_event(event)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    DashboardApp().run()

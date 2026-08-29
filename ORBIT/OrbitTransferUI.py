# ============================================================
# ORBIT TRANSFER UI
# ============================================================
#
# Pygame interface for OrbitTransfer.py
#
# Features:
#   • Search real macOS .app applications
#   • Launch selected apps
#   • Create saved app groups
#   • Add/remove apps from groups
#   • Open every app in a group
#   • Delete groups
#   • Refresh
#   • Mouse wheel scrolling
#   • ESC closes the UI
#
# Run this file:
#
#   python OrbitTransferUI.py
#
# ============================================================

import pygame
import OrbitTransfer


pygame.init()

WIDTH = 1200
HEIGHT = 760

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.RESIZABLE
)

pygame.display.set_caption("OrbitTransfer")

clock = pygame.time.Clock()

FONT = pygame.font.SysFont("SF Pro Display", 22)
SMALL_FONT = pygame.font.SysFont("SF Pro Display", 17)
TITLE_FONT = pygame.font.SysFont("SF Pro Display", 34, bold=True)
BUTTON_FONT = pygame.font.SysFont("SF Pro Display", 18, bold=True)

BACKGROUND = (245, 245, 247)
PANEL = (255, 255, 255)
BORDER = (215, 215, 220)
TEXT = (30, 30, 34)
SECONDARY = (105, 105, 112)
ACCENT = (60, 120, 245)
ACCENT_HOVER = (45, 103, 225)
DANGER = (220, 70, 70)
DANGER_HOVER = (195, 50, 50)


def draw_text(surface, text, font, x, y, colour=TEXT):
    image = font.render(str(text), True, colour)
    surface.blit(image, (x, y))


def draw_button(surface, rect, text, mouse_pos, danger=False):
    hovered = rect.collidepoint(mouse_pos)

    if danger:
        colour = DANGER_HOVER if hovered else DANGER
    else:
        colour = ACCENT_HOVER if hovered else ACCENT

    pygame.draw.rect(
        surface,
        colour,
        rect,
        border_radius=10
    )

    image = BUTTON_FONT.render(text, True, (255, 255, 255))
    surface.blit(
        image,
        image.get_rect(center=rect.center)
    )


def draw_card(surface, rect):
    pygame.draw.rect(
        surface,
        PANEL,
        rect,
        border_radius=14
    )

    pygame.draw.rect(
        surface,
        BORDER,
        rect,
        1,
        border_radius=14
    )


def truncate(text, max_chars):
    if len(text) <= max_chars:
        return text
    return text[:max_chars - 3] + "..."


class TextInput:

    def __init__(self, rect, placeholder=""):
        self.rect = pygame.Rect(rect)
        self.placeholder = placeholder
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return self.text
            elif event.unicode and event.unicode.isprintable():
                self.text += event.unicode

        return None

    def draw(self, surface):
        border_colour = ACCENT if self.active else BORDER

        pygame.draw.rect(
            surface,
            PANEL,
            self.rect,
            border_radius=10
        )

        pygame.draw.rect(
            surface,
            border_colour,
            self.rect,
            2,
            border_radius=10
        )

        display = self.text if self.text else self.placeholder
        colour = TEXT if self.text else SECONDARY

        draw_text(
            surface,
            display,
            FONT,
            self.rect.x + 14,
            self.rect.y + 10,
            colour
        )


class OrbitTransferUI:

    def __init__(self):
        self.running = True

        self.apps = []
        self.groups = {}

        self.selected_app = None
        self.selected_group = None

        self.search = TextInput(
            (30, 90, 470, 44),
            "Search applications..."
        )

        self.group_name = TextInput(
            (790, 90, 300, 44),
            "New group name..."
        )

        self.status = "OrbitTransfer ready."

        self.app_scroll = 0
        self.group_scroll = 0

        self.refresh()

    # ========================================================
    # DATA
    # ========================================================

    def refresh(self):
        self.apps = OrbitTransfer.find_apps()
        self.groups = OrbitTransfer.load_groups()

        if self.selected_app:
            names = [app["name"] for app in self.apps]
            if self.selected_app not in names:
                self.selected_app = None

        if self.selected_group:
            if self.selected_group not in self.groups:
                self.selected_group = None

        self.clamp_scroll()

    def filtered_apps(self):
        query = self.search.text.strip().lower()

        if not query:
            return self.apps

        return [
            app for app in self.apps
            if query in app["name"].lower()
        ]

    # ========================================================
    # ACTIONS
    # ========================================================

    def launch_selected(self):
        if not self.selected_app:
            self.status = "Select an application first."
            return

        self.status = OrbitTransfer.open_app(
            self.selected_app
        )

    def create_group(self):
        name = self.group_name.text.strip()

        if not name:
            self.status = "Enter a group name first."
            return

        self.status = OrbitTransfer.create_group(name)
        self.refresh()

        if name in self.groups:
            self.selected_group = name
            self.group_name.text = ""

    def add_selected_to_group(self):
        if not self.selected_app:
            self.status = "Select an application first."
            return

        if not self.selected_group:
            self.status = "Select a group first."
            return

        self.status = OrbitTransfer.add_to_group(
            self.selected_group,
            self.selected_app
        )

        self.refresh()

    def remove_selected_from_group(self):
        if not self.selected_app:
            self.status = "Select an application first."
            return

        if not self.selected_group:
            self.status = "Select a group first."
            return

        self.status = OrbitTransfer.remove_from_group(
            self.selected_group,
            self.selected_app
        )

        self.refresh()

    def open_selected_group(self):
        if not self.selected_group:
            self.status = "Select a group first."
            return

        self.status = OrbitTransfer.open_group(
            self.selected_group
        )

    def delete_selected_group(self):
        if not self.selected_group:
            self.status = "Select a group first."
            return

        name = self.selected_group
        self.status = OrbitTransfer.delete_group(name)

        self.selected_group = None
        self.refresh()

    # ========================================================
    # GEOMETRY
    # ========================================================

    def get_layout(self):
        width, height = screen.get_size()

        margin = 20
        gap = 20
        left_width = max(380, int(width * 0.43))
        right_x = margin + left_width + gap
        right_width = max(300, width - right_x - margin)

        top = 145
        bottom = height - 85
        card_height = max(200, bottom - top)

        return {
            "width": width,
            "height": height,
            "left": pygame.Rect(
                margin,
                top,
                left_width,
                card_height
            ),
            "right": pygame.Rect(
                right_x,
                top,
                right_width,
                card_height
            ),
        }

    def app_rect(self, index, card):
        return pygame.Rect(
            card.x + 15,
            card.y + 75 + index * 50 - self.app_scroll,
            card.width - 30,
            40
        )

    def group_rect(self, index, card):
        return pygame.Rect(
            card.x + 15,
            card.y + 75 + index * 50 - self.group_scroll,
            card.width - 30,
            40
        )

    def clamp_scroll(self):
        layout = self.get_layout()

        app_visible = max(100, layout["left"].height - 90)
        group_visible = max(100, layout["right"].height - 90)

        self.app_scroll = max(
            0,
            min(
                self.app_scroll,
                max(
                    0,
                    len(self.filtered_apps()) * 50 - app_visible
                )
            )
        )

        self.group_scroll = max(
            0,
            min(
                self.group_scroll,
                max(
                    0,
                    len(self.groups) * 50 - group_visible
                )
            )
        )

    # ========================================================
    # EVENTS
    # ========================================================

    def handle_event(self, event):
        search_result = self.search.handle_event(event)
        self.group_name.handle_event(event)

        if search_result is not None:
            self.search.text = search_result

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

            elif event.key == pygame.K_RETURN:
                if self.search.active:
                    self.launch_selected()

            elif event.key == pygame.K_r:
                self.refresh()
                self.status = "Application list refreshed."

        elif event.type == pygame.MOUSEWHEEL:
            mouse_x, _ = pygame.mouse.get_pos()
            layout = self.get_layout()

            if mouse_x < layout["right"].x:
                self.app_scroll -= event.y * 40
            else:
                self.group_scroll -= event.y * 40

            self.clamp_scroll()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)

    def handle_click(self, pos):
        layout = self.get_layout()

        # Buttons
        button_y = layout["height"] - 58

        launch_rect = pygame.Rect(30, button_y, 150, 40)
        add_rect = pygame.Rect(190, button_y, 150, 40)
        remove_rect = pygame.Rect(350, button_y, 150, 40)

        open_group_rect = pygame.Rect(
            layout["width"] - 390,
            button_y,
            130,
            40
        )

        delete_group_rect = pygame.Rect(
            layout["width"] - 250,
            button_y,
            130,
            40
        )

        refresh_rect = pygame.Rect(
            layout["width"] - 110,
            button_y,
            90,
            40
        )

        create_rect = pygame.Rect(
            layout["width"] - 92,
            90,
            72,
            44
        )

        if launch_rect.collidepoint(pos):
            self.launch_selected()
            return

        if add_rect.collidepoint(pos):
            self.add_selected_to_group()
            return

        if remove_rect.collidepoint(pos):
            self.remove_selected_from_group()
            return

        if open_group_rect.collidepoint(pos):
            self.open_selected_group()
            return

        if delete_group_rect.collidepoint(pos):
            self.delete_selected_group()
            return

        if refresh_rect.collidepoint(pos):
            self.refresh()
            self.status = "Application list refreshed."
            return

        if create_rect.collidepoint(pos):
            self.create_group()
            return

        # App selection
        visible_apps = self.filtered_apps()

        for index, app in enumerate(visible_apps):
            rect = self.app_rect(index, layout["left"])

            if rect.collidepoint(pos):
                self.selected_app = app["name"]
                return

        # Group selection
        group_names = list(self.groups.keys())

        for index, name in enumerate(group_names):
            rect = self.group_rect(index, layout["right"])

            if rect.collidepoint(pos):
                self.selected_group = name
                return

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self):
        screen.fill(BACKGROUND)

        layout = self.get_layout()
        width = layout["width"]
        height = layout["height"]

        draw_text(
            screen,
            "OrbitTransfer",
            TITLE_FONT,
            30,
            20
        )

        draw_text(
            screen,
            "Application launcher & groups",
            SMALL_FONT,
            30,
            58,
            SECONDARY
        )

        # Search box
        self.search.rect.x = 30
        self.search.rect.y = 90
        self.search.rect.width = max(
            250,
            layout["left"].width - 30
        )
        self.search.draw(screen)

        # Group name input + create
        group_input_width = min(
            300,
            max(170, layout["right"].width - 95)
        )

        self.group_name.rect.x = layout["right"].x
        self.group_name.rect.y = 90
        self.group_name.rect.width = group_input_width
        self.group_name.draw(screen)

        create_rect = pygame.Rect(
            width - 92,
            90,
            72,
            44
        )

        draw_button(
            screen,
            create_rect,
            "Create",
            pygame.mouse.get_pos()
        )

        # Cards
        draw_card(screen, layout["left"])
        draw_card(screen, layout["right"])

        # Headings
        draw_text(
            screen,
            "Applications",
            FONT,
            layout["left"].x + 18,
            layout["left"].y + 15
        )

        draw_text(
            screen,
            f"{len(self.filtered_apps())} found",
            SMALL_FONT,
            layout["left"].x + 18,
            layout["left"].y + 44,
            SECONDARY
        )

        draw_text(
            screen,
            "App Groups",
            FONT,
            layout["right"].x + 18,
            layout["right"].y + 15
        )

        draw_text(
            screen,
            f"{len(self.groups)} saved",
            SMALL_FONT,
            layout["right"].x + 18,
            layout["right"].y + 44,
            SECONDARY
        )

        # Apps
        old_clip = screen.get_clip()
        screen.set_clip(layout["left"])

        for index, app in enumerate(self.filtered_apps()):
            rect = self.app_rect(index, layout["left"])

            if not rect.colliderect(layout["left"]):
                continue

            selected = self.selected_app == app["name"]

            pygame.draw.rect(
                screen,
                ACCENT if selected else (238, 238, 242),
                rect,
                border_radius=9
            )

            draw_text(
                screen,
                truncate(app["name"], 40),
                SMALL_FONT,
                rect.x + 14,
                rect.y + 10,
                (255, 255, 255) if selected else TEXT
            )

        screen.set_clip(old_clip)

        # Groups
        old_clip = screen.get_clip()
        screen.set_clip(layout["right"])

        for index, name in enumerate(self.groups.keys()):
            rect = self.group_rect(index, layout["right"])

            if not rect.colliderect(layout["right"]):
                continue

            selected = self.selected_group == name

            pygame.draw.rect(
                screen,
                ACCENT if selected else (238, 238, 242),
                rect,
                border_radius=9
            )

            draw_text(
                screen,
                truncate(name, 35),
                SMALL_FONT,
                rect.x + 14,
                rect.y + 10,
                (255, 255, 255) if selected else TEXT
            )

        screen.set_clip(old_clip)

        # Status
        status_rect = pygame.Rect(
            20,
            height - 68,
            width - 40,
            48
        )

        pygame.draw.rect(
            screen,
            PANEL,
            status_rect,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            BORDER,
            status_rect,
            1,
            border_radius=10
        )

        draw_text(
            screen,
            truncate(self.status, 110),
            SMALL_FONT,
            status_rect.x + 14,
            status_rect.y + 8,
            SECONDARY
        )

        # Bottom buttons
        button_y = height - 58

        draw_button(
            screen,
            pygame.Rect(30, button_y, 150, 40),
            "Launch App",
            pygame.mouse.get_pos()
        )

        draw_button(
            screen,
            pygame.Rect(190, button_y, 150, 40),
            "Add to Group",
            pygame.mouse.get_pos()
        )

        draw_button(
            screen,
            pygame.Rect(350, button_y, 150, 40),
            "Remove",
            pygame.mouse.get_pos(),
            danger=True
        )

        draw_button(
            screen,
            pygame.Rect(width - 390, button_y, 130, 40),
            "Open Group",
            pygame.mouse.get_pos()
        )

        draw_button(
            screen,
            pygame.Rect(width - 250, button_y, 130, 40),
            "Delete Group",
            pygame.mouse.get_pos(),
            danger=True
        )

        draw_button(
            screen,
            pygame.Rect(width - 110, button_y, 90, 40),
            "Refresh",
            pygame.mouse.get_pos()
        )

        pygame.display.flip()

    # ========================================================
    # RUN
    # ========================================================

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(
                        event.size,
                        pygame.RESIZABLE
                    )
                else:
                    self.handle_event(event)

            self.clamp_scroll()
            self.draw()
            clock.tick(60)
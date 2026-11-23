#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:17:58 2026

@author: ethanbrown
"""
import time
from tkinter import font

import pygame
import Player
import Board
import Items
import music
import json
import sys
import os
import sys
import traceback
import Generator
import math
import random
import lava_sprites
import speech_bubble
import Enemies as Enemies_py
import shutil


class ImageManager:
    def __init__(self):
        """
        Loads all PNG and JPEG images from 'assets/images' upfront.
        Optimises them for performance based on transparency.
        """
        self.images = {}
        
        # Target the 'assets/images' directory relative to this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(base_dir, "assets", "images")
        
        # Fail-safe check
        if not os.path.exists(folder_path):
            raise FileNotFoundError(
                f"Could not find asset directory at: {folder_path}\n"
                f"Ensure your folder structure is: your_code.py -> assets/images/"
            )

        # Loop through all files in 'assets/images'
        for filename in os.listdir(folder_path):
            lower_name = filename.lower()
            
            # Filter for images
            if lower_name.endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(folder_path, filename)
                
                # Get the name without extension (e.g., 'knight_idle.png' -> 'knight_idle')
                image_key = os.path.splitext(filename)[0]
                
                try:
                    surface = pygame.image.load(file_path)
                    
                    # Custom conversion for alpha/non-alpha files
                    if lower_name.endswith('.png'):
                        self.images[image_key] = surface.convert_alpha()
                    else:
                        self.images[image_key] = surface.convert()
                        
                except pygame.error as e:
                    print(e)

    def load(self, name):
        """
        Retrieves a loaded surface by its filename (minus the extension) for blitting.
        """
        if name in self.images:
            return self.images[name]
        
        print(f"Warning: Image asset '{name}' not found.")
        return None

# Nausea effect
nausea_enabled = False
nausea_time = 0
nausea_ticks = 121

NAUSEA_SPEED = 5
NAUSEA_STRENGTH = 20
NAUSEA_ROTATION = 5

# Knight animation (frames come from the sliced sprite sheet: "knight walk 0", "knight sword 3", ...)
walk_time = 0
attack_time = 0
hurt_time = 99
last_hp = None
facing_left = False

WIZARD_HEIGHT = 70   # how tall the wizard sprite is on screen (the bubble sits this far above his feet)

WALK_TICKS = 8      # game ticks per walk frame
ATTACK_TICKS = 5    # game ticks per attack frame
HURT_TICKS = 7      # game ticks per hurt frame

# Which sheet frames play for each weapon (the others in the sheet are effect-only frames)
ATTACK_FRAMES = {
    "sword": [1, 2, 3, 4, 5, 6],
    "bow": [1, 2, 3, 4, 6],
    "flame": [1, 6, 1, 6],
}

SETTINGS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "settings.json"
)
CHARACTER_CLASSES = {
    "Knight": Player.Knight,
    "Pirate": Player.Pirate
}

def get_sign_text(level_name, place):
    with open(os.path.join("texts.json"), "r") as file:
        signs = json.load(file)

    for sign_name, sign_data in signs.items():
        if sign_data["level"] == level_name and sign_data["place"] == list(place):
            return sign_data["text"]

    return None

def load_settings():
    with open(SETTINGS_PATH, "r") as file:
        return json.load(file)

def save_settings(settings):
    with open(SETTINGS_PATH, "w") as file:
        json.dump(settings, file, indent=4)
        file.write("\n")

def change_setting(settings, setting_index):
    setting = settings["settings"][setting_index]

    if setting["type"] == "character":
        for other_setting in settings["settings"]:
            if other_setting["type"] == "character":
                other_setting["checked"] = False

    setting["checked"] = True if setting["type"] == "character" else not setting["checked"]
    save_settings(settings)

def selected_character(settings):
    for setting in settings["settings"]:
        if setting["type"] == "character" and setting["checked"]:
            return setting["character"]
    return "Knight"

def game_error(error_type, error, traceback_object):

    print(error_type)

    print(error)

    print(traceback_object)

    import pygame
    import traceback
    import random
    import sys

    pygame.init()

    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Steppefall - Technicians at Work")

    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("Arial", 42, bold=True)
    font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 16)
    error_font = pygame.font.SysFont("Courier New", 15)

    # =========================================================
    # ERROR
    # =========================================================

    full_error = "".join(
        traceback.format_exception(
            error_type,
            error,
            traceback_object
        )
    )

    # Split the traceback into lines
    error_lines = full_error.splitlines()

    # =========================================================
    # MODES
    # =========================================================

    mode = "menu"

    # =========================================================
    # SNAKE
    # =========================================================

    snake = [(400, 300), (380, 300), (360, 300)]
    snake_direction = (20, 0)

    snake_food = (
        random.randrange(1, WIDTH // 20) * 20,
        random.randrange(5, HEIGHT // 20) * 20
    )

    snake_timer = 0
    snake_score = 0

    # =========================================================
    # FLAPPY BIRD
    # =========================================================

    bird_x = 200
    bird_y = 300
    bird_velocity = 0

    gravity = 0.5
    flap_strength = -8

    pipe_x = WIDTH
    pipe_gap_y = 300
    pipe_width = 80
    pipe_gap = 180

    flappy_score = 0

    # =========================================================
    # ERROR VIEW SCROLL
    # =========================================================

    error_scroll = 0

    # =========================================================
    # BUTTONS
    # =========================================================

    snake_button = pygame.Rect(300, 330, 180, 60)
    flappy_button = pygame.Rect(520, 330, 180, 60)

    error_button = pygame.Rect(
        350,
        420,
        300,
        55
    )

    running = True

    while running:

        dt = clock.tick(60)

        # =====================================================
        # EVENTS
        # =====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            # =================================================
            # MENU
            # =================================================

            if mode == "menu":

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if snake_button.collidepoint(event.pos):

                        mode = "snake"

                        snake = [
                            (400, 300),
                            (380, 300),
                            (360, 300)
                        ]

                        snake_direction = (20, 0)

                        snake_score = 0

                    elif flappy_button.collidepoint(event.pos):

                        mode = "flappy"

                        bird_y = 300
                        bird_velocity = 0
                        pipe_x = WIDTH
                        flappy_score = 0

                    elif error_button.collidepoint(event.pos):

                        mode = "error"

                        error_scroll = 0

            # =================================================
            # ERROR VIEW
            # =================================================

            elif mode == "error":

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:

                        mode = "menu"

                    # Arrow keys
                    elif event.key == pygame.K_UP:

                        error_scroll -= 30

                    elif event.key == pygame.K_DOWN:

                        error_scroll += 30

                    elif event.key == pygame.K_PAGEUP:

                        error_scroll -= 300

                    elif event.key == pygame.K_PAGEDOWN:

                        error_scroll += 300

                # Mouse wheel
                elif event.type == pygame.MOUSEWHEEL:

                    error_scroll -= event.y * 30

            # =================================================
            # SNAKE
            # =================================================

            elif mode == "snake":

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:

                        if snake_direction != (0, 20):
                            snake_direction = (0, -20)

                    elif event.key == pygame.K_DOWN:

                        if snake_direction != (0, -20):
                            snake_direction = (0, 20)

                    elif event.key == pygame.K_LEFT:

                        if snake_direction != (20, 0):
                            snake_direction = (-20, 0)

                    elif event.key == pygame.K_RIGHT:

                        if snake_direction != (-20, 0):
                            snake_direction = (20, 0)

                    elif event.key == pygame.K_ESCAPE:

                        mode = "menu"

            # =================================================
            # FLAPPY
            # =================================================

            elif mode == "flappy":

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:

                        bird_velocity = flap_strength

                    elif event.key == pygame.K_ESCAPE:

                        mode = "menu"

        # =====================================================
        # MENU DRAWING
        # =====================================================

        if mode == "menu":

            screen.fill((18, 22, 28))

            title = title_font.render(
                "STEPPEFALL HAS CRASHED",
                True,
                (255, 100, 100)
            )

            screen.blit(
                title,
                title.get_rect(
                    center=(WIDTH // 2, 80)
                )
            )

            message = font.render(
                "The technicians are fixing it!",
                True,
                (255, 220, 100)
            )

            screen.blit(
                message,
                message.get_rect(
                    center=(WIDTH // 2, 150)
                )
            )

            sub = small_font.render(
                "While you wait, you can play:",
                True,
                (200, 200, 200)
            )

            screen.blit(
                sub,
                sub.get_rect(
                    center=(WIDTH // 2, 210)
                )
            )

            # Snake

            pygame.draw.rect(
                screen,
                (60, 150, 80),
                snake_button,
                border_radius=10
            )

            text = font.render(
                "SNAKE",
                True,
                (255, 255, 255)
            )

            screen.blit(
                text,
                text.get_rect(
                    center=snake_button.center
                )
            )

            # Flappy

            pygame.draw.rect(
                screen,
                (70, 130, 200),
                flappy_button,
                border_radius=10
            )

            text = font.render(
                "FLAPPY BIRD",
                True,
                (255, 255, 255)
            )

            screen.blit(
                text,
                text.get_rect(
                    center=flappy_button.center
                )
            )

            # Full error

            pygame.draw.rect(
                screen,
                (75, 75, 85),
                error_button,
                border_radius=10
            )

            text = font.render(
                "VIEW FULL ERROR",
                True,
                (255, 255, 255)
            )

            screen.blit(
                text,
                text.get_rect(
                    center=error_button.center
                )
            )

            # Error preview

            preview = str(error)

            if len(preview) > 90:

                preview = preview[:90] + "..."

            preview_surface = small_font.render(
                "Error: " + preview,
                True,
                (180, 180, 180)
            )

            screen.blit(
                preview_surface,
                preview_surface.get_rect(
                    center=(WIDTH // 2, 510)
                )
            )

        # =====================================================
        # FULL ERROR VIEW
        # =====================================================

        elif mode == "error":

            screen.fill((12, 14, 18))

            # Header

            pygame.draw.rect(
                screen,
                (25, 28, 35),
                (0, 0, WIDTH, 65)
            )

            title = title_font.render(
                "FULL ERROR",
                True,
                (255, 100, 100)
            )

            screen.blit(
                title,
                (20, 12)
            )

            back = small_font.render(
                "ESC = Back",
                True,
                (180, 180, 180)
            )

            screen.blit(
                back,
                (WIDTH - 110, 25)
            )

            # Error background

            error_area = pygame.Rect(
                20,
                85,
                WIDTH - 40,
                HEIGHT - 110
            )

            pygame.draw.rect(
                screen,
                (20, 22, 27),
                error_area,
                border_radius=8
            )

            # Calculate maximum scroll

            line_height = 19

            total_height = (
                len(error_lines) * line_height
            )

            visible_height = error_area.height - 20

            max_scroll = max(
                0,
                total_height - visible_height
            )

            error_scroll = max(
                0,
                min(error_scroll, max_scroll)
            )

            # Draw error

            y = (
                error_area.y
                + 10
                - error_scroll
            )

            for line in error_lines:

                if (
                    y > error_area.y - line_height
                    and y < error_area.bottom
                ):

                    # Highlight common traceback lines

                    if (
                        "Traceback" in line
                        or "Error:" in line
                        or "Exception" in line
                    ):

                        colour = (255, 110, 110)

                    elif "File " in line:

                        colour = (255, 210, 100)

                    else:

                        colour = (210, 215, 225)

                    surface = error_font.render(
                        line,
                        True,
                        colour
                    )

                    screen.blit(
                        surface,
                        (error_area.x + 10, y)
                    )

                y += line_height

            # Scroll bar

            if total_height > visible_height:

                bar_height = max(
                    40,
                    int(
                        visible_height
                        * visible_height
                        / total_height
                    )
                )

                bar_y = (
                    error_area.y
                    +
                    (
                        error_scroll
                        / max_scroll
                    )
                    * (
                        visible_height
                        - bar_height
                    )
                )

                pygame.draw.rect(
                    screen,
                    (90, 95, 105),
                    (
                        WIDTH - 28,
                        bar_y,
                        6,
                        bar_height
                    ),
                    border_radius=3
                )

        # =====================================================
        # SNAKE DRAWING
        # =====================================================

        elif mode == "snake":

            screen.fill((15, 25, 18))

            snake_timer += dt

            if snake_timer >= 110:

                snake_timer = 0

                head_x, head_y = snake[0]

                new_head = (
                    head_x + snake_direction[0],
                    head_y + snake_direction[1]
                )

                if (
                    new_head[0] < 0
                    or new_head[0] >= WIDTH
                    or new_head[1] < 65
                    or new_head[1] >= HEIGHT
                    or new_head in snake
                ):

                    mode = "menu"

                else:

                    snake.insert(
                        0,
                        new_head
                    )

                    if new_head == snake_food:

                        snake_score += 1

                        snake_food = (
                            random.randrange(
                                1,
                                WIDTH // 20
                            ) * 20,
                            random.randrange(
                                4,
                                HEIGHT // 20
                            ) * 20
                        )

                    else:

                        snake.pop()

            header = font.render(
                f"SNAKE    Score: {snake_score}    ESC = menu",
                True,
                (255, 255, 255)
            )

            screen.blit(
                header,
                (20, 15)
            )

            pygame.draw.rect(
                screen,
                (220, 70, 70),
                (
                    snake_food[0],
                    snake_food[1],
                    20,
                    20
                )
            )

            for segment in snake:

                pygame.draw.rect(
                    screen,
                    (80, 210, 100),
                    (
                        segment[0],
                        segment[1],
                        20,
                        20
                    ),
                    border_radius=4
                )

        # =====================================================
        # FLAPPY DRAWING
        # =====================================================

        elif mode == "flappy":

            screen.fill((100, 180, 240))

            bird_velocity += gravity
            bird_y += bird_velocity

            pipe_x -= 4

            if pipe_x < -pipe_width:

                pipe_x = WIDTH

                pipe_gap_y = random.randint(
                    170,
                    HEIGHT - 170
                )

                flappy_score += 1

            bird_rect = pygame.Rect(
                bird_x - 15,
                int(bird_y) - 15,
                30,
                30
            )

            pygame.draw.ellipse(
                screen,
                (255, 230, 60),
                bird_rect
            )

            top_pipe = pygame.Rect(
                pipe_x,
                0,
                pipe_width,
                pipe_gap_y - pipe_gap // 2
            )

            bottom_pipe = pygame.Rect(
                pipe_x,
                pipe_gap_y + pipe_gap // 2,
                pipe_width,
                HEIGHT
            )

            pygame.draw.rect(
                screen,
                (70, 180, 80),
                top_pipe
            )

            pygame.draw.rect(
                screen,
                (70, 180, 80),
                bottom_pipe
            )

            if (
                bird_rect.colliderect(top_pipe)
                or bird_rect.colliderect(bottom_pipe)
                or bird_y < 0
                or bird_y > HEIGHT
            ):

                mode = "menu"

            score_text = font.render(
                f"FLAPPY BIRD    Score: {flappy_score}    SPACE = flap    ESC = menu",
                True,
                (255, 255, 255)
            )

            screen.blit(
                score_text,
                (20, 15)
            )

        pygame.display.flip()

    pygame.quit()


sys.excepthook = game_error




#---------------code----------------





def start():
    pygame.init()
    pygame.font.init()
    icon = pygame.image.load("assets/images/Cover.png")
    pygame.display.set_icon(icon)
    current_screen = pygame.display.get_surface()
    size = current_screen.get_size() if current_screen else (1280, 720)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption("Steppefall")
    lava_sprites.load()
    return screen

def draw_inventory(game_surface, inventory_data, font):
    """Draw inventory panel on the left side"""

    panel_height = max(0, game_surface.get_height() - 50)
    pygame.draw.rect(game_surface, (30, 30, 50), (0, 50, 150, panel_height))
    pygame.draw.rect(game_surface, (100, 100, 150), (0, 50, 150, panel_height), 2)

    section = inventory_data['section']
    items = inventory_data['items']

    # -------------------------------------------------
    # ALWAYS keep the index valid
    # -------------------------------------------------
    if items:
        inventory_data['index'] = max(
            0,
            min(inventory_data['index'], len(items) - 1)
        )
    else:
        inventory_data['index'] = 0

    index = inventory_data['index']

    # -------------------------------------------------
    # Section colour
    # -------------------------------------------------
    section_colors = {
        'weapon': (255, 100, 100),
        'armour': (100, 150, 255),
        'item': (150, 255, 100)
    }

    color = section_colors.get(section, (255, 255, 255))

    # -------------------------------------------------
    # Title
    # -------------------------------------------------
    title = font.render(section.upper(), True, color)
    game_surface.blit(title, (10, 60))

    # -------------------------------------------------
    # Items
    # -------------------------------------------------
    y_pos = 90

    for i, item in enumerate(items[:25]):

        # Pointer
        if i == index:
            pygame.draw.rect(
                game_surface,
                (255, 255, 0),
                (5, y_pos - 2, 140, 20)
            )

            text = font.render(
                str(item)[:15],
                True,
                (0, 0, 0)
            )

        else:
            text = font.render(
                str(item)[:15],
                True,
                (200, 200, 200)
            )

        game_surface.blit(text, (10, y_pos))

        y_pos += 25

    # -------------------------------------------------
    # Empty inventory
    # -------------------------------------------------
    if not items:
        text = font.render(
            "Empty",
            True,
            (100, 100, 100)
        )

        game_surface.blit(text, (10, 90))

def level_complete(screen, levelNo):
    clock = pygame.time.Clock()
    menue = True
    while menue:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menue = False
        
        font = pygame.font.SysFont(None, 60)
        text = font.render(f"LEVEL {levelNo} COMPLETE", True, (0, 255, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text, text_rect)
        
        font = pygame.font.SysFont(None, 40)
        text = font.render("Press space to continue", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 70))
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(60)

def drawAll(screen, level, Player, bullets, hp, dam, coins, enemies, inventory_data=None,
             player_width=40, player_hight=40, boss=None, smokes=None,
             nausea_enabled=False, ticks=0, image_manager=None, speech=None, npcs=None):
    INVENTORY_WIDTH = 150
    TILE_SIZE = 40

    global nausea_time, walk_time, attack_time, hurt_time, last_hp, facing_left

    if smokes is None:
        smokes = []
    if npcs is None:
        npcs = []

    WIDTH, HEIGHT = screen.get_size()
    GAME_WIDTH = max(1, WIDTH - INVENTORY_WIDTH)
    game_surface = pygame.Surface((WIDTH, HEIGHT))

    # Calculate the camera offset directly instead of moving it one pixel
    # at a time in while loops.
    camera_left = GAME_WIDTH * 0.34
    camera_right = GAME_WIDTH * 0.66
    camera_top = HEIGHT * 0.31
    camera_bottom = HEIGHT * 0.625

    add_x = 0
    add_y = 0

    if Player.y > camera_bottom:
        add_y = -math.ceil(Player.y - camera_bottom)
    elif Player.y < camera_top:
        add_y = math.ceil(camera_top - Player.y) if Player.y < camera_top else 0
        # The original camera only moved upwards here when its offset was
        # already negative. At the start of this calculation it is zero.

    if Player.x > camera_right:
        add_x = -math.ceil(Player.x - camera_right)
    elif Player.x < camera_left:
        add_x = math.ceil(camera_left - Player.x) if Player.x < camera_left else 0

    # Keep the world from moving past its edges.
    if add_x > 0:
        add_x = 0
    elif len(level[0]) * TILE_SIZE + add_x < GAME_WIDTH:
        add_x = GAME_WIDTH - len(level[0]) * TILE_SIZE

    if add_y > 0:
        add_y = 0
    elif len(level) * TILE_SIZE + add_y < HEIGHT:
        add_y = HEIGHT - len(level) * TILE_SIZE

    cam_x = int(add_x)
    cam_y = int(add_y)

    game_surface.fill((0, 0, 0))

    # Keep scaled assets between frames. image_manager.load() is only called
    # when an asset/size is first needed.
    if not hasattr(drawAll, "_image_cache"):
        drawAll._image_cache = {}

    image_cache = drawAll._image_cache
    cache_prefix = id(image_manager)

    def get_image(name, size):
        key = (cache_prefix, name, size)
        if key not in image_cache:
            image_cache[key] = pygame.transform.scale(
                image_manager.load(name), size
            )
        return image_cache[key]

    game_surface.blit(get_image("background", (WIDTH, HEIGHT)), (0, 0))

    # Only visit the visible part of the level, with a small drawing buffer.
    start_y = max(0, (-cam_y) // TILE_SIZE - 3)
    end_y = min(len(level), (HEIGHT - cam_y) // TILE_SIZE + 3)
    start_x = max(0, (-cam_x) // TILE_SIZE - 3)
    end_x = min(len(level[0]), (GAME_WIDTH - cam_x) // TILE_SIZE + 3)

    lava_frame = lava_sprites.get_frame(ticks)

    background_tile = get_image("back ground", (160, 160))
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            if x % 4 == 0 and y % 4 == 0:
                game_surface.blit(
                    background_tile,
                    (INVENTORY_WIDTH + x * TILE_SIZE + cam_x,
                     y * TILE_SIZE + cam_y)
                )

    visited_cells = set()
    base_img = image_manager.load("block4")
    block_width = base_img.get_width() // 4
    block_height = base_img.get_height() // 4

    # Pre-scale the four-by-four block quadrants once, rather than creating
    # and scaling a new subsurface for every visible block on every frame.
    if not hasattr(drawAll, "_block_quadrants"):
        drawAll._block_quadrants = {}
    quadrant_key = (cache_prefix, base_img.get_width(), base_img.get_height())
    if quadrant_key not in drawAll._block_quadrants:
        drawAll._block_quadrants[quadrant_key] = [
            pygame.transform.scale(
                base_img.subsurface((
                    qx * block_width, qy * block_height,
                    block_width, block_height
                )),
                (TILE_SIZE, TILE_SIZE)
            )
            for qy in range(4) for qx in range(4)
        ]
    block_quadrants = drawAll._block_quadrants[quadrant_key]
    large_block = get_image("block4", (160, 160))

    # Frequently used tile sprites are loaded and scaled once.
    sulfur_img = get_image("sulfur deposit", (70, 70))
    drip_img = get_image("drip block", (80, 40))
    coin_img = get_image("coin", (40, 40))
    chest_img = get_image("chest", (40, 40))
    web_img = get_image("spider web", (40, 40))
    open_chest_img = get_image("open chest", (40, 40))
    vine_img = get_image("vine", (40, 40))
    vine_end_img = get_image("vine end", (40, 40))

    for y in range(start_y, end_y):
        row = level[y]
        for x in range(start_x, min(end_x, len(row))):
            if (x, y) in visited_cells:
                continue

            tile = row[x]
            pos_x = INVENTORY_WIDTH + x * TILE_SIZE + cam_x
            pos_y = y * TILE_SIZE + cam_y

            if tile == "B" or tile == "b":
                # Preserve the existing 4x4 detection rule.
                has_all = True
                for check_y in range(4):
                    check_row_y = y + check_y
                    if check_row_y >= len(level):
                        has_all = False
                        break
                    check_row = level[check_row_y]
                    if x + 4 > len(check_row):
                        has_all = False
                        break
                    for check_x in range(4):
                        if check_row[x + check_x] != "b":
                            has_all = False
                            break
                    if not has_all:
                        break

                if has_all:
                    game_surface.blit(large_block, (pos_x, pos_y))
                    for check_y in range(4):
                        for check_x in range(4):
                            visited_cells.add((x + check_x, y + check_y))
                else:
                    quadrant = (y % 4) * 4 + (x % 4)
                    game_surface.blit(block_quadrants[quadrant], (pos_x, pos_y))
                    visited_cells.add((x, y))

            elif tile == "M":
                game_surface.blit(sulfur_img, (pos_x - 20, pos_y + 10))

            elif tile == "D":
                game_surface.blit(drip_img, (pos_x, pos_y))

            elif isinstance(tile, str) and tile.startswith("L"):
                above = y > 0 and str(level[y - 1][x]).startswith("L")
                lava_sprites.draw_lava(
                    game_surface,
                    pos_x,
                    pos_y,
                    int(str(tile)[1:]),
                    above,
                    lava_frame
                )

            elif tile == "C":
                game_surface.blit(coin_img, (pos_x, pos_y))

            elif tile == "H":
                game_surface.blit(chest_img, (pos_x, pos_y))

            elif tile == "u":
                game_surface.blit(web_img, (pos_x, pos_y))

            elif tile == "K":
                game_surface.blit(open_chest_img, (pos_x, pos_y))

            elif tile == "P":
                if y + 1 < len(level) and x < len(level[y + 1]) and level[y + 1][x] == "P":
                    game_surface.blit(vine_img, (pos_x, pos_y))
                else:
                    game_surface.blit(vine_end_img, (pos_x, pos_y))

            elif isinstance(tile, str) and tile.startswith("W"):
                water_number = int(tile[1:])
                water_height = max(1, round(water_number * (TILE_SIZE / 14)))
                water_rect = pygame.Rect(
                    pos_x, pos_y + TILE_SIZE - water_height,
                    TILE_SIZE, water_height
                )
                pygame.draw.rect(game_surface, (20, 110, 220), water_rect)
                inner_rect = water_rect.inflate(-4, -2)
                if inner_rect.width > 0 and inner_rect.height > 0:
                    pygame.draw.rect(
                        game_surface, (100, 180, 255),
                        (inner_rect.x, inner_rect.y, inner_rect.width,
                         max(1, min(3, inner_rect.height // 2)))
                    )

    for smoke in smokes:
        pygame.draw.rect(
            game_surface, smoke.color,
            (INVENTORY_WIDTH + smoke.x + add_x, smoke.y + add_y, 40, 40)
        )

    for bullet in bullets:
        if bullet is not None:
            pygame.draw.rect(
                game_surface, (255, 255, 255),
                (INVENTORY_WIDTH + bullet.x + add_x, bullet.y + add_y,
                 bullet.size_width, bullet.size_width)
            )

    enemy_img = get_image("enemy", (60, 60))
    enemy_img_flipped = pygame.transform.flip(enemy_img, True, False)
    for enemy in enemies:
        img = enemy_img_flipped if enemy.going_left else enemy_img
        game_surface.blit(
            img,
            (INVENTORY_WIDTH + enemy.x + add_x - 7,
             enemy.y + add_y - 15)
        )

    if boss is not None:
        boss_rect = pygame.Rect(
            INVENTORY_WIDTH + boss.x + add_x, boss.y + add_y,
            boss.width, boss.hight
        )
        pygame.draw.rect(game_surface, (190, 35, 15), boss_rect)
        pygame.draw.rect(game_surface, (255, 130, 20), boss_rect.inflate(-12, -12))
        health_width = round(boss.width * max(0, boss.hp) / boss.max_hp)
        pygame.draw.rect(
            game_surface, (60, 0, 0),
            (boss_rect.x, boss_rect.y - 8, boss.width, 5)
        )
        pygame.draw.rect(
            game_surface, (255, 30, 20),
            (boss_rect.x, boss_rect.y - 8, health_width, 5)
        )
        for attack in boss.attackCurrents:
            pygame.draw.rect(
                game_surface, (255, 80, 0),
                (INVENTORY_WIDTH + attack.x + add_x, attack.y + add_y,
                 attack.size_width, attack.size_hight)
            )

    # Keep the existing special colours for the first two weapon bullets.
    if bullets and bullets[0] is not None:
        pygame.draw.rect(
            game_surface, (255, 100, 0),
            (INVENTORY_WIDTH + bullets[0].x + add_x,
             bullets[0].y + add_y,
             bullets[0].size_width, bullets[0].size_hight)
        )
    if len(bullets) > 1 and bullets[1] is not None:
        pygame.draw.rect(
            game_surface, (255, 200, 0),
            (INVENTORY_WIDTH + bullets[1].x + add_x,
             bullets[1].y + add_y,
             bullets[1].size_width, bullets[1].size_hight)
        )

    # Cache fonts as well: constructing SysFont objects every frame is wasteful.
    if not hasattr(drawAll, "_font_cache"):
        drawAll._font_cache = {}
    if 30 not in drawAll._font_cache:
        drawAll._font_cache[30] = pygame.font.SysFont(None, 30)
    if 24 not in drawAll._font_cache:
        drawAll._font_cache[24] = pygame.font.SysFont(None, 24)
    if 20 not in drawAll._font_cache:
        drawAll._font_cache[20] = pygame.font.SysFont(None, 20)

    font = drawAll._font_cache[30]
    text = font.render(str(hp), True, (255, 0, 0))
    game_surface.blit(text, text.get_rect(center=(WIDTH - 30, 30)))
    text = font.render(str(coins), True, (255, 255, 0))
    game_surface.blit(text, text.get_rect(center=(INVENTORY_WIDTH + 30, 30)))

    if dam:
        if not hasattr(drawAll, "_damage_overlay") or drawAll._damage_overlay.get_size() != (WIDTH, HEIGHT):
            drawAll._damage_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            drawAll._damage_overlay.fill((255, 0, 0, 100))
        game_surface.blit(drawAll._damage_overlay, (0, 0))

    if Player.equipped['weapon'] in ['Sword +3', 'Sword +1', 'Dagger +1']:
        weapon_set = "sword"
    elif Player.equipped['weapon'] in ['Bow +3', 'Bow']:
        weapon_set = "bow"
    elif Player.equipped['weapon'] == 'Flame Thrower':
        weapon_set = "flame"
    else:
        weapon_set = "sword"

    moved = Player.x - getattr(Player, "last_x", Player.x)
    if moved < 0:
        facing_left = True
    elif moved > 0:
        facing_left = False

    if last_hp is not None and hp < last_hp:
        hurt_time = 0
    last_hp = hp
    walk_time = walk_time + 1 if moved != 0 else 0
    frames = ATTACK_FRAMES[weapon_set]

    if attack_time > 0:
        attack_time += 1
    if attack_time == 0 and bullets and bullets[0] is not None:
        attack_time = 1
    if attack_time > len(frames) * ATTACK_TICKS:
        attack_time = 1 if bullets and bullets[0] is not None else 0

    if hurt_time < 6 * HURT_TICKS:
        image_name = f"knight hurt {hurt_time // HURT_TICKS}"
        hurt_time += 1
    elif attack_time > 0:
        image_name = f"knight {weapon_set} {frames[(attack_time - 1) // ATTACK_TICKS]}"
    elif moved != 0:
        image_name = f"knight walk {(walk_time // WALK_TICKS) % 6}"
    else:
        image_name = f"knight {weapon_set} 0"

    size = Player.hight + 44
    img = get_image(image_name, (size, size))
    if facing_left:
        flip_key = (cache_prefix, image_name, size, "flipped")
        if flip_key not in image_cache:
            image_cache[flip_key] = pygame.transform.flip(img, True, False)
        img = image_cache[flip_key]

    player_screen_x = INVENTORY_WIDTH + Player.x + add_x - (size - Player.width) // 2
    player_screen_y = Player.y + add_y - (size - Player.hight)
    game_surface.blit(img, (player_screen_x, player_screen_y))

    if speech:
        bubble_font = drawAll._font_cache[24]
        for npc_x, npc_y, npc_text in speech:
            speech_bubble.draw_speech_bubble(
                game_surface, image_manager, bubble_font, npc_text,
                INVENTORY_WIDTH + npc_x + 20 + add_x,
                npc_y + 40 - WIZARD_HEIGHT + add_y
            )

    wizard_img_cache = {}
    for npc in npcs:
        npc_size = (npc.width + 88, npc.hight + 50)
        if npc_size not in wizard_img_cache:
            wizard_img_cache[npc_size] = get_image("wizard", npc_size)
        game_surface.blit(
            wizard_img_cache[npc_size],
            (INVENTORY_WIDTH + npc.x + add_x - 40, npc.y + add_y - 40)
        )

    if inventory_data:
        draw_inventory(game_surface, inventory_data, drawAll._font_cache[20])

    if nausea_enabled:
        nausea_time += 1 / 40
        wobble_x = math.sin(nausea_time * NAUSEA_SPEED) * NAUSEA_STRENGTH
        wobble_y = math.cos(nausea_time * NAUSEA_SPEED) * NAUSEA_STRENGTH
        angle = math.sin(nausea_time * NAUSEA_SPEED) * NAUSEA_ROTATION
        rotated = pygame.transform.rotate(game_surface, angle)
        rotated_rect = rotated.get_rect(
            center=(WIDTH // 2 + wobble_x, HEIGHT // 2 + wobble_y)
        )
        screen.fill((0, 0, 0))
        screen.blit(rotated, rotated_rect)
    else:
        screen.blit(game_surface, (0, 0))

    return screen



def map(screen, map_x_scroll, mouse_click=None):
    width, height = screen.get_size()

    # -------------------------------------------------
    # COLOURS
    # -------------------------------------------------

    background = (13, 16, 23)
    cave_colour = (23, 28, 37)
    cave_highlight = (37, 43, 53)
    path_shadow = (65, 55, 43)
    path_colour = (160, 125, 77)
    normal_colour = (105, 119, 130)
    normal_highlight = (180, 193, 198)
    boss_colour = (180, 55, 25)
    boss_highlight = (255, 125, 40)
    white = (235, 230, 215)

    # -------------------------------------------------
    # FONTS
    # -------------------------------------------------

    title_font = pygame.font.SysFont(None, 58)
    room_font = pygame.font.SysFont(None, 27)
    small_font = pygame.font.SysFont(None, 23)

    # -------------------------------------------------
    # LOAD DISCOVERED ROOMS
    # -------------------------------------------------

    with open("world_save.json", "r") as file:
        world_data = json.load(file)

    world = world_data.get("world", {})

    if not isinstance(world, dict):
        world = {}

    normal_rooms = world.get("normal_rooms_found", [])
    boss_rooms = world.get("boss_rooms_completed", [])

    if not isinstance(normal_rooms, list):
        normal_rooms = []

    if not isinstance(boss_rooms, list):
        boss_rooms = []

    destinations = []

    for room_name in normal_rooms:
        if isinstance(room_name, str):
            destinations.append(room_name)

    if "Fire Boss Room" in boss_rooms:
        destinations = [
            room for room in destinations
            if room != "Level 20"
        ]

        destinations.append("Fire Boss Room")

    # -------------------------------------------------
    # SORT ROOMS
    # -------------------------------------------------

    def map_room_order(room_name):

        if room_name == "Fire Boss Room":
            return 20

        if room_name.startswith("Level "):
            try:
                return int(room_name.split(" ")[1])
            except ValueError:
                return 9999

        return 9999

    destinations.sort(key=map_room_order)

    # -------------------------------------------------
    # BACKGROUND
    # -------------------------------------------------

    screen.fill(background)

    # Cave ceiling
    pygame.draw.polygon(
        screen,
        cave_colour,
        [
            (0, 0),
            (width, 0),
            (width, 120),
            (width - 100, 145),
            (width - 230, 115),
            (width - 380, 155),
            (width - 520, 120),
            (0, 150)
        ]
    )

    # Cave floor
    pygame.draw.polygon(
        screen,
        cave_colour,
        [
            (0, height),
            (width, height),
            (width, height - 90),
            (width - 180, height - 115),
            (width - 350, height - 85),
            (width - 500, height - 120),
            (0, height - 90)
        ]
    )

    # Small cave details
    for i in range(35):

        x = (i * 173) % width
        y = 170 + ((i * 97) % max(1, height - 300))

        pygame.draw.circle(
            screen,
            cave_highlight,
            (x, y),
            2
        )

    # -------------------------------------------------
    # TITLE
    # -------------------------------------------------

    title = title_font.render(
        "THE UNDERGROUND",
        True,
        white
    )

    screen.blit(title, (40, 25))

    subtitle = small_font.render(
        "KNOWN PASSAGES AND DISCOVERED ROOMS",
        True,
        (145, 151, 155)
    )

    screen.blit(subtitle, (43, 78))

    # -------------------------------------------------
    # ROOM POSITIONS
    # -------------------------------------------------

    room_positions = []

    room_heights = [
        310,
        420,
        290,
        390,
        330
    ]

    for i, room_name in enumerate(destinations):

        x = 130 + i * 230 - map_x_scroll
        y = room_heights[i % len(room_heights)]

        room_positions.append((x, y, room_name))

    # -------------------------------------------------
    # CONNECTING PATHS
    # -------------------------------------------------

    for i in range(len(room_positions) - 1):

        x1, y1, name1 = room_positions[i]
        x2, y2, name2 = room_positions[i + 1]

        middle_x = (x1 + x2) // 2
        middle_y = (y1 + y2) // 2

        if i % 2 == 0:
            middle_y += 45
        else:
            middle_y -= 45

        points = [
            (x1, y1),
            (middle_x, middle_y),
            (x2, y2)
        ]

        # Dark outline
        pygame.draw.lines(
            screen,
            path_shadow,
            False,
            points,
            18
        )

        # Actual path
        pygame.draw.lines(
            screen,
            path_colour,
            False,
            points,
            7
        )

    # -------------------------------------------------
    # ROOM MARKERS
    # -------------------------------------------------

    for i, room_data in enumerate(room_positions):

        x, y, room_name = room_data

        boss_room = room_name == "Fire Boss Room"

        if boss_room:
            colour = boss_colour
            highlight = boss_highlight
            radius = 35
        else:
            colour = normal_colour
            highlight = normal_highlight
            radius = 29

        # Hover detection
        marker_rect = pygame.Rect(
            x - 42,
            y - 42,
            84,
            84
        )

        label_rect = pygame.Rect(
            x - 90,
            y + 48,
            180,
            45
        )

        hovered = (
            marker_rect.collidepoint(pygame.mouse.get_pos())
            or label_rect.collidepoint(pygame.mouse.get_pos())
        )

        if hovered:
            radius += 5

        # Outer ring
        pygame.draw.circle(
            screen,
            highlight,
            (x, y),
            radius + 7
        )

        # Main marker
        pygame.draw.circle(
            screen,
            colour,
            (x, y),
            radius
        )

        # Centre
        pygame.draw.circle(
            screen,
            highlight,
            (x, y),
            9
        )

        # Room label background
        pygame.draw.rect(
            screen,
            (25, 29, 37),
            label_rect,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            highlight,
            label_rect,
            2,
            border_radius=6
        )

        label = room_font.render(
            room_name,
            True,
            white
        )

        screen.blit(
            label,
            label.get_rect(center=label_rect.center)
        )

        # Special boss label
        if boss_room:

            boss_text = small_font.render(
                "BOSS",
                True,
                boss_highlight
            )

            screen.blit(
                boss_text,
                boss_text.get_rect(
                    center=(x, y - 53)
                )
            )

        # Clicking a room
        if mouse_click is not None:

            if marker_rect.collidepoint(mouse_click):
                return room_name

            if label_rect.collidepoint(mouse_click):
                return room_name

    # -------------------------------------------------
    # FOOTER
    # -------------------------------------------------

    pygame.draw.rect(
        screen,
        (20, 24, 32),
        (0, height - 48, width, 48)
    )

    instructions = small_font.render(
        "A / D or LEFT / RIGHT = MOVE MAP     |     M = CLOSE MAP",
        True,
        (180, 185, 190)
    )

    screen.blit(
        instructions,
        instructions.get_rect(
            center=(width // 2, height - 24)
        )
    )



def death(screen):
    menue = True
    quitting = []
    while menue:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menue = False
                    quitting = [True, False, False]
                if event.key == pygame.K_ESCAPE:
                    menue = False
                    quitting = [False, False, False]
        font = pygame.font.SysFont(None, 60)  # Default font, size 60
        text = font.render("You died    WOMP WOMP WOMP WOMP", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2,
                                          screen.get_height() // 2))
        screen.blit(text, text_rect)
        text = font.render("Press space to play again", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2,
                                          screen.get_height() // 2 + 70))
        screen.blit(text, text_rect)
        text = font.render("Press escape to return to the main menu", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2,
                                          screen.get_height() // 2 + 100))
        screen.blit(text, text_rect)
        pygame.display.flip()
    return quitting

def settings_menu(screen, settings):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)
    title_font = pygame.font.SysFont(None, 60)
    width, height = screen.get_size()
    back_button = pygame.Rect((width - 280) // 2, height - 80, 280, 60)
    checkbox_buttons = []
    scroll = 0
    running = True

    while running:
        width, height = screen.get_size()
        back_button.centerx = width // 2
        back_button.top = height - 80
        screen.fill((30, 30, 30))
        title = title_font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(width // 2, 100)))

        checkbox_buttons = []
        for index, setting in enumerate(settings["settings"]):
            y_pos = 150 + (index * 50) - scroll
            if 125 <= y_pos <= height - 130:
                checkbox = pygame.Rect(width // 2 - 240, y_pos, 35, 35)
                checkbox_buttons.append((checkbox, index))
                #(70, 100, 160)
                pygame.draw.rect(screen, (0, 0, 0), checkbox, border_radius=5)
                if setting["checked"]:
                    pygame.draw.rect(screen, (0, 255, 0), checkbox.inflate(-10, -10))

                question = font.render(setting["question"], True, (255, 255, 255))
                screen.blit(question, (checkbox.right + 20, y_pos + 4))

        pygame.draw.rect(screen, (80, 80, 80), back_button, border_radius=10)
        back_text = font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    scroll = max(0, scroll - 50)
                elif event.key == pygame.K_DOWN:
                    max_scroll = max(0, len(settings["settings"]) * 50 - (height - 255))
                    scroll = min(max_scroll, scroll + 50)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and back_button.collidepoint(event.pos):
                    running = False
                elif event.button == 1:
                    for checkbox, index in checkbox_buttons:
                        if checkbox.collidepoint(event.pos):
                            change_setting(settings, index)
                elif event.button == 4:
                    scroll = max(0, scroll - 50)
                elif event.button == 5:
                    max_scroll = max(0, len(settings["settings"]) * 50 - (height - 255))
                    scroll = min(max_scroll, scroll + 50)

        pygame.display.flip()
        clock.tick(60)

    return settings
    

def run():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
                
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))   
    screen = start()
    image_manager = ImageManager()
    font = pygame.font.SysFont(None, 30)
    settings = load_settings()
    while True:
        menu = True

        while menu:
            width, height = screen.get_size()

            screen.fill((30, 30, 30))

            # =========================
            # BUTTONS
            # =========================

            play_button = pygame.Rect((width - 280) // 2, height // 2 - 60, 280, 70)
            settings_button = pygame.Rect((width - 280) // 2, height // 2 + 40, 280, 70)

            pygame.draw.rect(screen, (60, 120, 70), play_button, border_radius=10)
            pygame.draw.rect(screen, (70, 100, 160), settings_button, border_radius=10)

            text = font.render("Play", True, (255, 255, 255))
            text_rect = text.get_rect(center=play_button.center)
            screen.blit(text, text_rect)

            text = font.render("Settings", True, (255, 255, 255))
            text_rect = text.get_rect(center=settings_button.center)
            screen.blit(text, text_rect)

            # =========================
            # EVENTS
            # =========================

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if play_button.collidepoint(event.pos):

                        menu = False

                    elif settings_button.collidepoint(event.pos):

                        settings = settings_menu(screen, settings)

            pygame.display.flip()

        round = True
        while round:
            runwin = True
            
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))   

            levelNo = 1

            


            screen = start()  
            music.play_music("audio (1).mp3")
            level = [24, 24]
            player_class = CHARACTER_CLASSES.get(selected_character(settings), Player.Knight)
            player_1 = player_class(level)
            clock = pygame.time.Clock()
            
            while runwin:
                num = str(levelNo)

                if levelNo == 20:
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    levels_dir = os.path.join(base_dir, "assets", "levels")
                    source_file = os.path.join(levels_dir, "level40A.txt")
                    destination_file = os.path.join(levels_dir, "level20.txt")
                    shutil.copyfile(source_file, destination_file)

                
                with open(
                    os.path.join(BASE_DIR, 'assets', 'levels', f'level{levelNo}.txt'),
                    'r'
                ) as file:
                    level = [list(line.rstrip('\r\n')) for line in file]

                level_name = f"level{levelNo}"

                print("Lava positions:")

                for y in range(len(level)):
                    for x in range(len(level[y])):
                        if level[y][x] == "L":
                            print("Lava at:", x, y)

                for i in range(len(level)):
                    for j in range(len(level[i])):
                        if level[i][j] == "S":
                            player_1.x = j * 40
                            player_1.y = i * 40
                            break

                for i in range(len(level)):
                    for j in range(len(level[i])):
                        if level[i][j] == "L":
                            level[i][j] = "L7"

                for i in range(len(level)):
                    for j in range(len(level[i])):
                        if level[i][j] == "W":
                            level[i][j] = "W14"

                print(level)
                
                player_1.level = level
                LAVA_SPEED = 20
                player_1.timefrozen = False
                player_1.timefrozenat = None
                player_1.on_fire_for = None
                player_1.on_fire = False
                player_1.jumps = 0
                won = None
                running = True
                aBoard = Board.board(level)
                ticks = 0
                lastHp = player_1.hp
                pointOfDamage = 21
                dam = False
                a = aBoard.findPoint("S")
                player_1.x = a[0]
                player_1.y = a[1]
                enemies = aBoard.spawn(levelNo)
                speech = []
                npcs = []
                for y in range(len(level)):
                    for x in range(len(level[y])):
                        if level[y][x] == 'n':
                            npc = Enemies_py.NPC(level, 'Wizard', ['Hello contestant', 'Give me 3 gold keys and i will bestow a gift apon you', 'Khan is nearing, hurry', "I live in this cave", "I am a wizard", "You can find me here later", "I can help you"])
                            npc.x = x * 40
                            npc.y = y * 40
                            npcs.append(npc)
                bosses = aBoard.BossSpawn()
                extraa = False
                boss = None
                if bosses is not None:
                    boss = bosses
                holding_attack = False
                holding_super_attack = False
                

                nausea_ticks = 1210000000

                room1 = False
                room2 = False

                text_show = False

                Generator.run(f"level{str(levelNo + 1)}", levelNo + 1)

                if levelNo == 20:
                    with open("world_save.json", "r") as file:
                        world_data = json.load(file)

                    world = world_data.get("world")
                    if not isinstance(world, dict):
                        world = {}
                        world_data["world"] = world

                    boss_rooms = world.get("boss_rooms_completed")
                    if not isinstance(boss_rooms, list):
                        boss_rooms = []
                        world["boss_rooms_completed"] = boss_rooms

                    if "Fire Boss Room" not in boss_rooms:
                        boss_rooms.append("Fire Boss Room")

                    with open("world_save.json", "w") as file:
                        json.dump(world_data, file)
                else:
                    with open("world_save.json", "r") as file:
                        world_data = json.load(file)

                    world = world_data.get("world")
                    if not isinstance(world, dict):
                        world = {}
                        world_data["world"] = world

                    normal_rooms = world.get("normal_rooms_found")
                    if not isinstance(normal_rooms, list):
                        normal_rooms = []
                        world["normal_rooms_found"] = normal_rooms

                    room_name = f"Level {levelNo}"
                    if room_name not in normal_rooms:
                        normal_rooms.append(room_name)
                    
                    with open("world_save.json", "w") as file:
                        json.dump(world_data, file)
                
                map_show = False

                was_map_show = False

                map_x_scroll = 0

                while running:

                    simulation_start = time.perf_counter()
                    map_click_pos = None


                    #helpfull for stomping on enemies heads
                    player_1.last_x = player_1.x
                    player_1.last_y = player_1.y
                    
                    #events
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()                    
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                player_1.hp = 0
                            if event.key == pygame.K_q:
                                room1 = True
                            if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                                player_1.jump()
                            if event.key == pygame.K_LCTRL or event.key == pygame.K_z:
                                holding_attack = True
                            if event.key == pygame.K_LSHIFT or event.key == pygame.K_x:
                                holding_super_attack = True
                            if event.key == pygame.K_c:
                                player_1.level = level
                                player_1.use_item(enemies + ([boss] if boss is not None else []))
                                level = player_1.level
                            if event.key == pygame.K_v:
                                player_1.switch_inventory_section()
                            if event.key == pygame.K_m:
                                map_show = not map_show
                            if event.key == pygame.K_e:
                                for npc in npcs:
                                    if npc.is_near_player(player_1):
                                        npc.next_line()
                                pos = aBoard.getPlayerBlocks(x=player_1.x, y=player_1.y)
                                found_sign = False

                                for tile in pos:
                                    try:
                                        if level[tile[1]][tile[0]] == "s":
                                            text_show = not text_show
                                            found_sign = True
                                            break
                                    except (IndexError, TypeError):
                                        pass

                                if not found_sign:
                                    text_show = False
                            
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_LCTRL or event.key == pygame.K_z:
                                holding_attack = False
                            if event.key == pygame.K_LSHIFT or event.key == pygame.K_x:
                                holding_super_attack = False
                            if event.key == pygame.K_q:
                                room1 = False
                                    
                        if event.type == pygame.MOUSEWHEEL:
                            if event.y > 0:
                                player_1.scroll_inventory(-1)  # Up scrolls up in list
                            elif event.y < 0:
                                player_1.scroll_inventory(1)   # Down scrolls down in list
                            
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 2:  # Middle mouse button
                                player_1.switch_inventory_section()
                            elif event.button == 1:  # Left mouse button to equip
                                if map_show:
                                    map_click_pos = event.pos
                                else:
                                    player_1.equip_item(enemies + ([boss] if boss is not None else []))
                        
                    #movement
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        if map_show:
                            map_x_scroll -= 20
                        else:
                            player_1.move(True, False)
                    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        if map_show:
                            map_x_scroll += 20
                        else:
                            player_1.move(False, True)
                    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                        player_1.climb_down()

                    mouse_pos = pygame.mouse.get_pos()

                    if map_show and not was_map_show:
                        map_x_scroll = 0

                    aBoard.level = level

                    if bosses is not None:
                        boss.level = level
                    
                    player_1.level = level
                    
                    for i in range(len(enemies)):
                        enemies[i].level = level
                    
                    #fire
                    player_1.FireTick(ticks)
                    
                    #weapon attacks
                    if player_1.attack_cooldown > 0:
                        player_1.attack_cooldown -= 1
                    if (holding_attack and player_1.current_attack is None
                            and player_1.attack_cooldown == 0):
                        player_1.attack()
                        player_1.attack_cooldown = player_1.attack_interval()
                    if holding_super_attack and player_1.current_super is None and player_1.super_charged:
                        player_1.super_attack()

                    player_1.update_attacks(holding_attack, holding_super_attack, extraa, enemies)
                    extraa = False
                    
                    #fall out the world death
                    if player_1.y > len(level) * 40:
                        player_1.hp = 0
                    
                    #collect coins
                    coins_collected = player_1.collect_coins()
                    if coins_collected:
                        player_1.recharge_super(coins_collected)
                        
                    #damage flash, no, not that type
                    if settings["settings"][2]["checked"] == True:
                        if player_1.hp < lastHp:
                            dam = True
                            pointOfDamage = 0
                            lastHp = player_1.hp
                        if pointOfDamage <= 20 and dam:
                            pointOfDamage += 1
                        if pointOfDamage > 20:
                            pointOfDamage = 21
                            dam = False
                    
                    #player death
                    if player_1.death():
                        death_result = death(screen)
                        round = death_result[0]
                        runwin = death_result[1]
                        won = False
                    elif player_1.hp > lastHp:
                        lastHp = player_1.hp
                    
                    #End level
                    if player_1.is_on_wall(block="E", Or=True):
                        level_complete(screen, levelNo)
                        running = False
                    
                    #player gravity
                    player_1.update_vy()

                    player_1.level = level
                    player_1.WaterTick()
                    player_1.spider_webs()
            
                    if player_1.timefrozen:
                        if player_1.timefrozenat is None:
                            player_1.timefrozenat = ticks
                        elif ticks - player_1.timefrozenat >= (40 * player_1.timefrozen_duration):
                            player_1.timefrozen = False
                            player_1.timefrozenat = None
            
                    if not player_1.timefrozen:
                        #enemy updates
                        i = 0
                        while i < len(enemies):
                            enemy = enemies[i]
                        
                            enemy.update_vy()
                            enemy.level = level
                            enemy.move(ticks, Player=player_1)
                            level = enemy.level
                        
                            # Check weapon hits
                            hit_by_weapon = False
                            weapon_damage = player_1.get_attack_damage()
                            
                            if player_1.current_attack is not None:
                                if player_1.current_attack.is_touching_enemy(enemy.x, enemy.y):
                                    enemy.take_damage(weapon_damage)
                                    player_1.gain_coins(5)
                                    if enemy.hp <= 0:
                                        hit_by_weapon = True
                                        player_1.killed_enemies()
                            
                            if player_1.current_super is not None:
                                if player_1.current_super.is_touching_enemy(enemy.x, enemy.y):
                                    enemy.take_damage(weapon_damage)
                                    player_1.gain_coins(10)
                                    if enemy.hp <= 0:
                                        hit_by_weapon = True
                                        player_1.killed_enemies()
                            
                            if hit_by_weapon:
                                enemies.pop(i)
                                continue
                        
                            result = enemy.isTouchingPlayer(player_1)
                        
                            if result == "stomp":
                                player_1.vy = -10
                                player_1.gain_coins(3)
                                enemies.pop(i)
                                player_1.killed_enemies()
                                continue
                        
                            elif result == "hit":
                                player_1.take_damage(1)
                                enemies.pop(i)
                                player_1.killed_enemies()
                                continue
            
                            if enemy.hp <= 0:
                                enemies.pop(i)
                                player_1.killed_enemies()
                                continue
                        
                            i += 1

                        was_boss = False

                        if bosses is not None:
                            was_boss = True
                            print(boss.hp)
                            boss.update_vy()
                            boss.run(player_1.x, player_1.y)

                            boss.being_damaged = False

                            weapon_damage = player_1.get_attack_damage()

                            for attack_name in ("current_attack", "current_super"):
                                attack = getattr(player_1, attack_name)
                                if attack is not None and boss.is_touching_weapon(attack):
                                    boss.take_damage(weapon_damage)
                                    player_1.gain_coins(1)
                                    setattr(player_1, attack_name, None)
                                    boss.being_damaged = True
                                    if boss.hp <= 0:
                                        player_1.killed_enemies()
                                        was_boss = False
                                        bosses = None
                                        boss = None
                                        break

                            if bosses is not None:
                                for attack in boss.attackCurrents[:]:
                                    if boss.is_attack_touching_player(attack, player_1):
                                        player_1.take_damage(2)
                                        boss.attackCurrents.remove(attack)

                                result = boss.isTouchingPlayer(player_1)
                                if result == "stomp":
                                    player_1.vy = -10
                                    player_1.gain_coins(3)
                                    boss.take_damage(2)
                                    boss.being_damaged = True
                                elif result == "hit":
                                    if boss.contact_cooldown == 0:
                                        player_1.take_damage(1)
                                        boss.take_damage(1)
                                        boss.contact_cooldown = 40
                                        boss.being_damaged = True

                                if boss.hp <= 0:
                                    player_1.killed_enemies()
                                    was_boss = False
                                    bosses = None
                                    boss = None

                    if not was_boss:
                        for y in range(len(level)):
                            for x in range(len(level[y])):
                                if level[y][x] == 'p':
                                    level[y][x] = 'P'

                    player_1.level = level
                    player_1.broken_blocks()
                    level = player_1.level

                    #open chests
                    a = aBoard.getPlayerBlocks(x=player_1.x, y=player_1.y)
                    for i in range(len(a)):
                        try:
                            if level[a[i][1]][a[i][0]] == "H":
                                aBoard.setPoint(a[i][0], a[i][1], tile="K")
                                contents = aBoard.find_chest_contents()
                                if contents[0] == "10 Coins":
                                    coins_gained = player_1.gain_coins(10)
                                    player_1.recharge_super(coins_gained)
                                else:
                                    player_1.AppendInventory(contents[0])
                                if contents[1] == "10 Coins":
                                    coins_gained = player_1.gain_coins(10)
                                    player_1.recharge_super(coins_gained)
                                else:
                                    player_1.AppendInventory(contents[1])
                        except IndexError:
                            print("Player is out of bounds, but this should not happen. Killing the player to prevent further issues.")
                            player_1.hp = 0
                        except Exception as e:
                            print(f"An unexpected error occurred while checking for chests: {e}")
                    
                    # Prepare inventory data for display
                    inventory_data = {
                        'section': player_1.inventory_section,
                        'items': player_1.inventory[player_1.inventory_section],
                        'index': player_1.inventory_index[player_1.inventory_section]
                    }

                    if ticks % LAVA_SPEED == 0:
                        start_laval = time.perf_counter()

                        level = aBoard.lava_tick()

                        print("Lava:", ((time.perf_counter() - start_laval) * 1000, 2), "ms")

                        player_1.level = level

                        for i in range(len(enemies)):
                            enemies[i].level = level


                    WATER_SPEED = 10
                    if ticks % WATER_SPEED == 0:
                        start_water = time.perf_counter()

                        level = aBoard.water_tick()

                        print("Water:", ((time.perf_counter() - start_water) * 1000, 2), "ms")

                        player_1.level = level


                    level = aBoard.lava_drain()

                    if bosses is not None:
                        boss.level = level

                    player_1.level = level

                    for i in range(len(enemies)):
                        enemies[i].level = level

                    surrounding_tiles = aBoard.getPlayerBlocks(x=player_1.x, y=player_1.y)

                    room2 = False
                    for tile in surrounding_tiles:
                        try:
                            if level[tile[1]][tile[0]] == "R":
                                print("I found a secret room on level", levelNo, "at coordinates:", tile[0], tile[1])
                                room2 = True
                                if room2 and (room1 or player_1.secret_room_unlocked):
                                    print("Player has entered the secret room on level", levelNo)
                                    player_1.recharge_super(50)
                                    player_1.x = 200
                                    player_1.y = 200
                                    room1 = False
                                    room2 = False
                                    player_1.secret_room_unlocked = False
                                    room = None

                                    with open(os.path.join("assets", "levels", "secret rooms.txt"), "r") as file:
                                        for line in file:
                                            line = line.strip()

                                            if line.startswith(str(levelNo)):
                                                room = line[len(str(levelNo)):] + ".txt"
                                                break
                                    with open(
                                        os.path.join(BASE_DIR, 'assets', 'levels', room),
                                        'r'
                                    ) as file:
                                            level = [list(line.rstrip('\r\n')) for line in file]
                                            level_name = room[:-4]
                                    levelNo -= 1
                                pass
                        except IndexError:
                            pass
                    
                    if text_show:
                        font = pygame.font.SysFont(None, 30)
                        text = font.render("Press E to hide this text", True, (255, 255, 255))
                        screen.blit(text, (10, 10))
                        pos = aBoard.getPlayerBlocks(x=player_1.x, y=player_1.y)
                        for i in range(len(pos)):
                            if level[pos[i][1]][pos[i][0]] == "s":
                                write = get_sign_text(
                                    level_name,
                                (tile[0], tile[1])
                                )
                        text = font.render(write, True, (255, 255, 255))
                        screen.blit(text, (10, 100))

                    aBoard.rarity_weights = {"common": 60, "uncommon": 30, "rare": 10, "very rare": 1}
                    aBoard.rarity_weights["common"] += 1*player_1.luck
                    aBoard.rarity_weights["uncommon"] += 2*player_1.luck
                    aBoard.rarity_weights["rare"] += 3*player_1.luck
                    aBoard.rarity_weights["very rare"] += 4*player_1.luck

                    smokes = aBoard.sulpher()

                    to_pop = []
                    for i in range(len(smokes)):
                        if smokes[i].isTouchingPlayer(player_1):
                            nausea_ticks = 0
                            if random.random() < 0.5:
                                player_1.hp -= 1
                            to_pop.append(i)

                    for i in range(len(to_pop)):
                        smokes.pop(len(to_pop) - 1 - i)

                    nausea_ticks += 1
                    if nausea_ticks < 200:
                        nausea_enabled = True
                    else:
                        nausea_enabled = False

                    player_1.ticks += 1

                    simulation_time = time.perf_counter() - simulation_start

                    speech = [(npc.x, npc.y, npc.text()) for npc in npcs if npc.is_near_player(player_1)]

                    rendering_start = time.perf_counter()

                    if map_show:
                        map_return = map(screen, map_x_scroll, mouse_click=map_click_pos)

                        if map_return is not None:
                            level_name = map_return

                            if level_name == "Fire Boss Room":
                                levelNo = 19
                            else:
                                levelNo = int(level_name.split(" ")[1]) - 1

                            running = False
                    else:
                        screen = drawAll(
                            screen, level, player_1,
                            bullets=[player_1.current_attack, player_1.current_super],
                            hp=player_1.hp, dam=dam, coins=player_1.coins,
                            enemies=enemies, inventory_data=inventory_data,
                            player_width=player_1.width, player_hight=player_1.hight,
                            boss=boss if bosses is not None else None, smokes=smokes, nausea_enabled=nausea_enabled, ticks=ticks, image_manager=image_manager, speech=speech, npcs=npcs
                        )

                    was_map_show = map_show

                    if text_show:
                        screen.fill((0, 0, 0))

                        font = pygame.font.SysFont(None, 30)

                        text = font.render("Press E to hide this text", True, (255, 255, 255))
                        screen.blit(text, (10, 10))

                        write = "No sign text found."

                        pos = aBoard.getPlayerBlocks(x=player_1.x, y=player_1.y)

                        for tile in pos:
                            try:
                                if level[tile[1]][tile[0]] == "s":
                                    write = get_sign_text(
                                        level_name,
                                        (tile[0], tile[1])
                                    )
                                    break
                            except IndexError:
                                pass

                        if write is None:
                            write = "No sign text found."

                        text = font.render(write, True, (255, 255, 255))
                        screen.blit(text, (10, 100))

                    rendering_time = time.perf_counter() - rendering_start


                    pygame.display.flip()
                    clock.tick(40)
                    ticks += 1

                    if won is not None:
                        running = False
                if won is not False:
                    won = True
            
                if won:
                    levelNo += 1
                else:
                    runwin = False

run()
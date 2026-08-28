#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:17:58 2026

@author: ethanbrown
"""
import pygame
import Player
import Board
import Items
import sys
import os
import sys
import traceback

def game_error(error_type, error, traceback_object):

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



def start():
    pygame.init()
    pygame.font.init()
    icon = pygame.image.load("assets/images/Cover.png")
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Steppefall")
    return screen

def draw_inventory(screen, inventory_data, font):
    """Draw inventory panel on the left side"""
    pygame.draw.rect(screen, (30, 30, 50), (0, 50, 150, 670))
    pygame.draw.rect(screen, (100, 100, 150), (0, 50, 150, 670), 2)
    
    section = inventory_data['section']
    items = inventory_data['items']
    index = inventory_data['index']
    
    section_colors = {'weapon': (255, 100, 100), 'armour': (100, 150, 255), 'item': (150, 255, 100)}
    color = section_colors.get(section, (255, 255, 255))
    
    title = font.render(section.upper(), True, color)
    screen.blit(title, (10, 60))
    
    y_pos = 90
    for i, item in enumerate(items[:10]):
        if i == index:
            pygame.draw.rect(screen, (255, 255, 0), (5, y_pos - 2, 140, 20))
            text = font.render(item[:15], True, (0, 0, 0))
        else:
            text = font.render(item[:15], True, (200, 200, 200))
        screen.blit(text, (10, y_pos))
        y_pos += 25
    
    if not items:
        text = font.render("Empty", True, (100, 100, 100))
        screen.blit(text, (10, 90))

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

def drawAll(screen, level, player_x, player_y, bullets, hp, dam, coins, enemies, inventory_data=None):
    INVENTORY_WIDTH = 150
    GAME_WIDTH = 1280 - INVENTORY_WIDTH
    
    add = [0, 0]
    contemplating = True
    while contemplating:
        if (player_y + add[1]) > 600 or ((player_y + add[1]) < 120 and add[1] < 0):
            if (player_y + add[1]) > 600:
                add[1] -= 1
            else:
                add[1] += 1
        else:
            contemplating = False
    contemplating = True
    while contemplating:
        if (player_x + add[0]) > 750 or ((player_x + add[0]) < 380 and player_x < 380):
            if (player_x + add[0]) > 750:
                add[0] -= 1
            else:
                add[0] += 1
        else:
            contemplating = False
    if add[0] > 0:
        add[0] = 0
    elif len(level[0]) * 40 + add[0] < GAME_WIDTH:
        add[0] = GAME_WIDTH - len(level[0]) * 40

    if add[1] > 0:
        add[1] = 0
    elif len(level) * 40 + add[1] < 720:
        add[1] = 720 - len(level) * 40
        
    # Draw game area with inventory panel offset
    screen.fill((0, 0, 0))

    img = pygame.image.load("assets/images/firescene2.jpeg")
    img = pygame.transform.scale(img, (1280, 720))
    screen.blit(img, (0, 0))
    
    # Draw game world shifted right by inventory width
    pygame.draw.rect(screen, (0, 0, 255), (INVENTORY_WIDTH + player_x + add[0], player_y + add[1], 40, 40))
    
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "B":
                pygame.draw.rect(screen, (0,255,0), (INVENTORY_WIDTH + x*40+add[0], y*40+add[1], 40, 40))
            elif level[y][x] == "L":
                pygame.draw.rect(screen, (255,0,0), (INVENTORY_WIDTH + x*40+add[0], y*40+add[1], 40, 40))
            elif level[y][x] == "C":
                pygame.draw.rect(screen, (255,255,0), (INVENTORY_WIDTH + x*40+add[0], y*40+add[1], 40, 40))
            elif level[y][x] == "H":
                pygame.draw.rect(screen, (150, 75, 0), (INVENTORY_WIDTH + x*40+add[0], y*40+add[1], 40, 40))
                
    for i in range(len(bullets)):
        if bullets[i] is not None:
            pygame.draw.rect(screen, (255, 255, 255), (INVENTORY_WIDTH + bullets[i].x+add[0], bullets[i].y+add[1], bullets[i].size_width, bullets[i].size_width))
    
    for i in range(len(enemies)):
        pygame.draw.rect(screen, (0, 255, 255), (INVENTORY_WIDTH + enemies[i].x+add[0], enemies[i].y+add[1], 40, 40))
    
    # Draw weapon attacks
    if bullets[0] is not None:
        pygame.draw.rect(screen, (255, 100, 0), (INVENTORY_WIDTH + bullets[0].x+add[0], bullets[0].y+add[1], bullets[0].size_width, bullets[0].size_hight))
    if bullets[1] is not None:
        pygame.draw.rect(screen, (255, 200, 0), (INVENTORY_WIDTH + bullets[1].x+add[0], bullets[1].y+add[1], bullets[1].size_width, bullets[1].size_hight))
    
    # Draw UI stats (shifted for inventory panel)
    font = pygame.font.SysFont(None, 30)
    text = font.render(str(hp), True, (255, 0, 0))
    text_rect = text.get_rect(center=(INVENTORY_WIDTH + 1100, 30))
    screen.blit(text, text_rect)
    text = font.render(str(coins), True, (255, 255, 0))
    text_rect = text.get_rect(center=(INVENTORY_WIDTH + 30, 30))
    screen.blit(text, text_rect)
    if dam:
        damage = pygame.Surface((1280, 720), pygame.SRCALPHA)
        damage.fill((255, 0, 0, 100))
        screen.blit(damage, (0, 0))
    
    # Draw inventory panel (fixed, not affected by camera)
    if inventory_data:
        draw_inventory(screen, inventory_data, pygame.font.SysFont(None, 20))
    
    return screen

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
                if event.key == pygame.ESCAPE:
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
    

def run():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
                
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))   
    screen = start()
    font = pygame.font.SysFont(None, 30)
    while True:
        menu = True

        while menu:

            screen.fill((30, 30, 30))

            # =========================
            # BUTTONS
            # =========================

            play_button = pygame.Rect(500, 300, 280, 70)

            pygame.draw.rect(screen, (60, 120, 70), play_button, border_radius=10)

            text = font.render("Play", True, (255, 255, 255))
            text_rect = text.get_rect(center=play_button.center)
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

            pygame.display.flip()

        round = True
        while round:
            runwin = True
            
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))   

            levelNo = 1

            screen = start()  
            level = [24, 24]
            player_1 = Player.Pirate(level)
            clock = pygame.time.Clock()

            while runwin:
                num = str(levelNo)
                
                with open(
                    os.path.join(BASE_DIR, 'assets', 'levels', f'level{levelNo}.txt'),
                    'r'
                ) as file:
                    level = [list(line.rstrip('\r\n')) for line in file]

                player_1.level = level
                player_1.hp = 3
                player_1.timefrozen = False
                player_1.timefrozenat = None
                player_1.on_fire_for = None
                player_1.on_fire = False
                player_1.coins = 0
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
                enemies = aBoard.spawn()
                holding_attack = False
                holding_super_attack = False
                while running:
                    #helpfull for stomping on enemies heads
                    player_1.last_x = player_1.x
                    player_1.last_y = player_1.y
                    
                    #events
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()                    
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                player_1.jump()
                            if event.key == pygame.K_LCTRL or event.key == pygame.K_z:
                                holding_attack = True
                            if event.key == pygame.K_LSHIFT or event.key == pygame.K_x:
                                holding_super_attack = True
                            if event.key == pygame.K_c:
                                player_1.use_item(enemies)
                            
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_LCTRL or event.key == pygame.K_z:
                                holding_attack = False
                            if event.key == pygame.K_LSHIFT or event.key == pygame.K_x:
                                holding_super_attack = False
                                    
                        if event.type == pygame.MOUSEWHEEL:
                            if event.y > 0:
                                player_1.scroll_inventory(-1)  # Up scrolls up in list
                            elif event.y < 0:
                                player_1.scroll_inventory(1)   # Down scrolls down in list
                            
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 2:  # Middle mouse button
                                player_1.switch_inventory_section()
                            elif event.button == 1:  # Left mouse button to equip
                                player_1.equip_item(enemies)
                        
                    #movement
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        player_1.move(True, False)
                    if keys[pygame.K_RIGHT]:
                        player_1.move(False, True)
                    
                    #fire
                    player_1.FireTick(ticks)
                    
                    #weapon attacks
                    if holding_attack and player_1.current_attack is None:
                        player_1.attack()
                    if holding_super_attack and player_1.current_super is None and player_1.super_charged:
                        player_1.super_attack()
                    
                    player_1.update_attacks(holding_attack, holding_super_attack)
                    
                    #fall out the world death
                    if player_1.y > len(level) * 40:
                        player_1.hp = 0
                    
                    #collect coins
                    if player_1.collect_coins():
                        player_1.recharge_super(1)
                        
                    #damage flash, no, not that type
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
                    
                    #End level
                    if player_1.is_on_wall(block="E", Or=True):
                        level_complete(screen, levelNo)
                        running = False
                    
                    #player gravity
                    player_1.update_vy()
            
                    if player_1.timefrozen:
                        if player_1.timefrozenat is None:
                            player_1.timefrozenat = ticks
                        elif ticks - player_1.timefrozenat >= (40 * 15):  # 15 seconds at 40 ticks per second
                            player_1.timefrozen = False
                            player_1.timefrozenat = None
            
                    if not player_1.timefrozen:
                        #enemy updates
                        i = 0
                        while i < len(enemies):
                            enemy = enemies[i]
                        
                            enemy.update_vy()
                            enemy.move(ticks)
                        
                            # Check weapon hits
                            hit_by_weapon = False
                            weapon_damage = player_1.damage
                            
                            # Add weapon damage if equipped
                            if player_1.equipped.get('weapon'):
                                try:
                                    weapon_item = Items.Item(player_1.equipped['weapon'])
                                    weapon_damage += weapon_item.get_damage()
                                except:
                                    pass
                            
                            if player_1.current_attack is not None:
                                if player_1.current_attack.is_touching_enemy(enemy.x, enemy.y):
                                    enemy.take_damage(weapon_damage)
                                    player_1.coins += 5
                                    if enemy.hp <= 0:
                                        hit_by_weapon = True
                            
                            if player_1.current_super is not None:
                                if player_1.current_super.is_touching_enemy(enemy.x, enemy.y):
                                    enemy.take_damage(weapon_damage * 2)
                                    player_1.coins += 10
                                    if enemy.hp <= 0:
                                        hit_by_weapon = True
                            
                            if hit_by_weapon:
                                enemies.pop(i)
                                continue
                        
                            result = enemy.isTouchingPlayer(player_1)
                        
                            if result == "stomp":
                                player_1.vy = -10
                                player_1.coins += 3
                                enemies.pop(i)
                                continue
                        
                            elif result == "hit":
                                player_1.take_damage(1)
                                enemies.pop(i)
                                continue
            
                            if enemy.hp <= 0:
                                enemies.pop(i)
                                continue
                        
                            i += 1
                    
                    #open chests
                    a = aBoard.getPlayerBlocks(x=player_1.x, y=player_1.y)
                    for i in range(len(a)):
                        try:
                            if level[a[i][1]][a[i][0]] == "H":
                                aBoard.setPoint(a[i][0], a[i][1], tile=".")
                                contents = aBoard.find_chest_contents()
                                if contents[0] == "10 Coins":
                                    player_1.coins += 10
                                else:
                                    player_1.AppendInventory(contents[0])
                                if contents[1] == "10 Coins":
                                    player_1.coins += 10
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
                    
                    screen = drawAll(screen, level, player_x=player_1.x, player_y=player_1.y, bullets=[player_1.current_attack, player_1.current_super], hp=player_1.hp, dam=dam, coins=player_1.coins, enemies=enemies, inventory_data=inventory_data)
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
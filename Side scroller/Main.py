#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:17:58 2026

@author: ethanbrown
"""
import pygame
import Player
import Board
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('assets/levels/level1.txt', 'r') as file:
    level = [list(line.rstrip('\r\n')) for line in file]

#Window = 1280 × 720

global BASE_DIR

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def start():
    icon = pygame.image.load("assets/images/Cover.png")
    pygame.display.set_icon(icon)
    pygame.init()
    pygame.font.init()
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
    while menue:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menue = False
        font = pygame.font.SysFont(None, 60)  # Default font, size 60
        text = font.render("You died    WOMP WOMP WOMP WOMP", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2,
                                          screen.get_height() // 2))
        screen.blit(text, text_rect)
        text = font.render("Press space to play again", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() // 2,
                                          screen.get_height() // 2 + 70))
        screen.blit(text, text_rect)
        pygame.display.flip()

def run(level):
    selection = None
    aBoard = Board.board(level)
    aBoard.find_chest_contents()
    screen = start()
    player_1 = Player.Pirate(level)
    running = True
    clock = pygame.time.Clock()
    ticks = 0
    lastHp =player_1.hp
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
                    player_1.equip_item()
        
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
            death(screen)
            return False
        
        #End level
        if player_1.is_on_wall(block="E", Or=True):
            running = False
        
        #player gravity
        player_1.update_vy()
        
        #enemy updates
        i = 0
        while i < len(enemies):
            enemy = enemies[i]
        
            enemy.update_vy()
            enemy.move(ticks)
        
            # Check weapon hits
            hit_by_weapon = False
            if player_1.current_attack is not None:
                if player_1.current_attack.is_touching_enemy(enemy.x, enemy.y):
                    player_1.coins += 5
                    hit_by_weapon = True
            
            if player_1.current_super is not None:
                if player_1.current_super.is_touching_enemy(enemy.x, enemy.y):
                    player_1.coins += 10
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
                player_1.hp -= 1
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
    return True

levelNo = 1
while True:
    num = str(levelNo)
    
    with open(
        os.path.join(BASE_DIR, 'assets', 'levels', f'level{levelNo}.txt'),
        'r'
    ) as file:
        level = [list(line.rstrip('\r\n')) for line in file]
    if run(level):
        levelNo += 1
    else:
        levelNo = 1
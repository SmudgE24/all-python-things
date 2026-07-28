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

with open('assets/levels/level1.txt', 'r') as file:
    level = [list(line.rstrip('\r\n')) for line in file]

#Window = 1280 × 720

def start():
    icon = pygame.image.load("assets/images/Cover.png")
    pygame.display.set_icon(icon)
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Steppefall")
    return screen

def drawAll(screen, level, player_x, player_y, bullets, hp, dam, coins, enemies):
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
        if (player_x + add[0]) > 900 or ((player_x + add[0]) < 380 and player_x < 380):
            if (player_x + add[0]) > 900:
                add[0] -= 1
            else:
                add[0] += 1
        else:
            contemplating = False
    if add[0] > 0:
        add[0] = 0
    elif len(level[0]) * 40 + add[0] < 1280:
        add[0] = 1280 - len(level[0]) * 40

    if add[1] > 0:
        add[1] = 0
    elif len(level) * 40 + add[1] < 720:
        add[1] = 720 - len(level) * 40
        
        
        
        
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 0, 255), (player_x+add[0], player_y+add[1], 40, 40))
    
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "B":
                pygame.draw.rect(screen, (0,255,0), (x*40+add[0], y*40+add[1], 40, 40))
            elif level[y][x] == "L":
                pygame.draw.rect(screen, (255,0,0), (x*40+add[0], y*40+add[1], 40, 40))
            elif level[y][x] == "C":
                pygame.draw.rect(screen, (255,255,0), (x*40+add[0], y*40+add[1], 40, 40))
            elif level[y][x] == "H":
                pygame.draw.rect(screen, (150, 75, 0), (x*40+add[0], y*40+add[1], 40, 40))
                
    for i in range(len(bullets)):
        if bullets[i] is not None:
            pygame.draw.rect(screen, (255, 255, 255), (bullets[i].x+add[0], bullets[i].y+add[1], bullets[i].size_width, bullets[i].size_width))
    
    for i in range(len(enemies)):
        pygame.draw.rect(screen, (0, 255, 255), (enemies[i].x+add[0], enemies[i].y+add[1], 40, 40))
    
    
    font = pygame.font.SysFont(None, 30)
    text = font.render(str(hp), True, (255, 0, 0))
    text_rect = text.get_rect(center=(1250, 30))
    screen.blit(text, text_rect)
    text = font.render(str(coins), True, (255, 255, 0))
    text_rect = text.get_rect(center=(30, 30))
    screen.blit(text, text_rect)
    if dam:
        damage = pygame.Surface((1280, 720), pygame.SRCALPHA)
        damage.fill((255, 0, 0, 100))
        screen.blit(damage, (0, 0))
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
                    
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    print("Scrolled up")
                elif event.y < 0:
                    print("Scrolled down")
        
        #movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_1.move(True, False)
        if keys[pygame.K_RIGHT]:
            player_1.move(False, True)
        
        #fire
        player_1.FireTick(ticks)
        
        #fall out the world death
        if player_1.y > len(level) * 40:
            player_1.hp = 0
        
        #collect coins
        player_1.collect_coins()
            
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
        
        screen = drawAll(screen, level, player_x=player_1.x, player_y=player_1.y, bullets=[player_1.current_attack, player_1.current_super], hp=player_1.hp, dam=dam, coins=player_1.coins, enemies=enemies)
        pygame.display.flip()
        clock.tick(40)
        ticks += 1
    return True

levelNo = 1
while True:
    num = str(levelNo)
    with open(f'assets/levels/level{num}.txt', 'r') as file:
        level = [list(line.rstrip('\r\n')) for line in file]
    if run(level):
        levelNo += 1
    else:
        levelNo = 1
a = Board.board([])
a.find_chest_contents()
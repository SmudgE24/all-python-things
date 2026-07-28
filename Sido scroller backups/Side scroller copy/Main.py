#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:17:58 2026

@author: ethanbrownhello
"""
import random
import pygame
import Player

B = 'B'
A = '.'
L = 'L'

level = [
    [A, A, A, A, B, A, A],
    [A, A, A, A, B, A, A],
    [A, A, A, A, B, A, A],
    [A, A, A, A, B, A, A],
    [A, A, A, A, B, A, A],
    [A, A, A, A, B, A, A],
    [B, L, L, B, B, B, B],
    [A, A, A, A, B, A, A],
    [A, A, A, A, A, A, A],
    [A, A, A, A, A, A, A],
]
#tile size = 40 x 40

#Window = 1280 × 720

#player size = 40 x 40



class board:
    def __init__(self, level):
        self.level = level
        self.airs = []
        self.blocks = []
        self.lavas = []
        self.fires = []
        self.chests = []
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == '.':
                    self.airs.append((j, i))
                elif level[i][j] == 'B':
                    self.blocks.append((j, i))
                elif level[i][j] == 'L':
                    self.lavas.append((j, i))
                elif level[i][j] == 'F':
                    self.fires.append((j, i))
                elif level[i][j] == 'H':
                    self.chests.append((j, i))
    
    def find_chest_contents(self):
        items = ["10 Coins", "Jump boots", "Bow", "+1 life", "Void boots", "Shield +1", "Armour +1", "Armour +2", "Bomb", "Bottle o' healin", "Sword +3", "Key", "Time Freeze 15s", "Flame Gun", "Orb of power +5", "Dagger +1"]
        raraty = [60, 15, 10, 1, 2, 8, 7, 5, 20, 7, 12, 1, 3, 4, 1, 10]
        sum_of = 0
        for i in range(len(raraty)):
            sum_of += raraty[i]
            
        pickednumber1 = random.randint(0, sum_of)
        pickednumber2 = random.randint(0, sum_of)
        two = []
        for number in [pickednumber1, pickednumber2]:
            current_weight = 0
            for iteration in range(len(raraty)):
                current_weight += raraty[iteration]
                if number <= current_weight:
                    two.append(items[iteration])
                    break
        print(two)
        
    #def 

def start():
    icon = pygame.image.load("assets/images/Cover.png")
    pygame.display.set_icon(icon)
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((900, 900))
    pygame.display.set_caption("Steppefall")
    return screen

def drawAll(screen, level, player_x, player_y, bullets):
    wy = 160
    pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, 40, 40))
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "B":
                pygame.draw.rect(screen, (0,255,0), (x*40, y*40+wy, 40, 40))
            elif level[y][x] == "L":
                pygame.draw.rect(screen, (255,0,0), (x*40, y*40+wy, 40, 40))
    for i in range(len(bullets)):
        if bullets[i] is not None:
            pygame.draw.rect(screen, (255, 255, 255), (bullets[i].x, bullets[i].y+wy, bullets[i].size_width, bullets[i].size_width))
    return screen


random.seed() 

def run(level):
    aBoard = board(level)
    aBoard.find_chest_contents()
    screen = start()
    player_1 = Player.Pirate(level)
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_1.jump()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_1.move(True, False)
        if keys[pygame.K_RIGHT]:
            player_1.move(False, True)
        
        player_1.update_vy()
        screen = drawAll(screen, level, player_x=player_1.x, player_y=player_1.y, bullets=[player_1.current_attack, player_1.current_super])
        pygame.display.flip()
        clock.tick(40)
            

run(level)
a = board([])
a.find_chest_contents()
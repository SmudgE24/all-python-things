#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:17:58 2026

@author: ethanbrownhello
"""
import pygame
import Player
import Board

B = 'B'
A = '.'
L = 'L'

level = [
    [A, A, A, A, A, A, A],
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
    pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, 40, 40))
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "B":
                pygame.draw.rect(screen, (0,255,0), (x*40, y*40, 40, 40))
            elif level[y][x] == "L":
                pygame.draw.rect(screen, (255,0,0), (x*40, y*40, 40, 40))
    for i in range(len(bullets)):
        if bullets[i] is not None:
            pygame.draw.rect(screen, (255, 255, 255), (bullets[i].x, bullets[i].y, bullets[i].size_width, bullets[i].size_width))
    return screen




def run(level):
    aBoard = Board.board(level)
    aBoard.find_chest_contents()
    screen = start()
    player_1 = Player.Pirate(level)
    running = True
    clock = pygame.time.Clock()
    ticks = 0
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
        
        player_1.FireTick(ticks)
        
        print(player_1.on_fire)
        
        player_1.update_vy()
        screen = drawAll(screen, level, player_x=player_1.x, player_y=player_1.y, bullets=[player_1.current_attack, player_1.current_super])
        pygame.display.flip()
        clock.tick(40)
        ticks += 1
            

run(level)
a = Board.board([])
a.find_chest_contents()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:24:46 2026

@author: ethanbrown
"""
import os
import pygame
import drawing

def main_menue(screen, events, mouse_click):
    width, height = screen.get_size()
    pygame.draw.rect(screen, (255, 255, 255), (-5, -5, width + 10, (height // 10)+4))
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    opening_path = os.path.join(BASE_DIR, "assets/battery.png")
    opening_original = pygame.image.load(opening_path).convert()
    opening = pygame.transform.scale(opening_original, (width // 10, height // 10))
    screen.blit(opening, (width - (2*(width//10)), 0))
    drawing.draw_line(screen, (155, 155, 155), (-5, (height // 10)), ((width + 10), (height // 10)), 5)
    drawing.draw_line(screen, (55, 55, 55), (-5, (height // 10)+5), ((width + 10), (height // 10)+5), 5)
    drawing.text_blit(screen, (0, 0, 0), 100, "ORBIT", 5, 5)
    

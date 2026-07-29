#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 17:01:42 2026

@author: ethanbrown
"""

import pygame

pygame.init()

def Error(message, importance, screen=pygame.display.set_mode((1280, 720))):
    font = pygame.font.SysFont("couriernew", 15)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        text = font.render(f"There has been an error, the error is: {message} It is an importace of {str(importance)}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(640, 30))
        screen.blit(text, text_rect)
        
        pygame.display.flip()
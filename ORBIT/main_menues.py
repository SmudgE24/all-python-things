#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:24:46 2026

@author: ethanbrown
"""
import os
import pygame
import drawing
import subprocess
import re

def main_menue(screen, events, mouse_click=None):
    screen.fill((0, 0, 0))
    battery = subprocess.run(
    ["pmset", "-g", "batt"],
    capture_output=True,
    text=True
    )

    battery = re.search(r"(\d+)%", battery.stdout)

    if battery:
        battery = int(battery.group(1))
    
    width, height = screen.get_size()
    pygame.draw.rect(screen, (255, 255, 255), (-5, -5, width + 10, (height // 10)+4))
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    opening_path = os.path.join(BASE_DIR, "assets/battery.png")
    opening_original = pygame.image.load(opening_path).convert()
    opening = pygame.transform.scale(opening_original, (width // 10, height // 10))
    screen.blit(opening, (width - (2*(width//10)+100), 0))
    drawing.draw_line(screen, (155, 155, 155), (-5, (height // 10)), ((width + 10), (height // 10)), 5)
    drawing.draw_line(screen, (55, 55, 55), (-5, (height // 10)+5), ((width + 10), (height // 10)+5), 5)
    drawing.text_blit(screen, (0, 0, 0), 100, "ORBIT", 5, 5)

    drawing.text_blit(screen, (0, 0, 0), 90, f"%{battery}", width - (1*(width//10)+100), 0)

    terminalClick = drawing.draw_and_click_button(screen, 300, 300, "Terminal", 79, (255, 255, 255), (0, 75, 25), mouse_click)

    sentinelClick = drawing.draw_and_click_button(screen, 800, 300, "Sentinel", 79, (255, 255, 255), (0, 75, 25), mouse_click)

    transferClick = drawing.draw_and_click_button(screen, 300, 450, "Transfer", 79, (255, 255, 255), (0, 75, 25), mouse_click)

    schedulerClick = drawing.draw_and_click_button(screen, 800, 450, "Schedulerr", 79, (255, 255, 255), (0, 75, 25), mouse_click)

    if terminalClick:
        return "terminal_launch"
    elif sentinelClick:
        return "sentinel_launch"
    elif transferClick:
        return "transfer_launch"
    elif schedulerClick:
        return "scheduler_launch"

    return "none"

    
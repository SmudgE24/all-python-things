#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:56:19 2026

@author: ethanbrown
"""

import pygame
import Orbit_open
import Errors
import main_menues

print("TEST")

#Start up
try:
    screen = Orbit_open.start(Orbit_open.lines)
except Exception as e:
    print(f"Opening Error: {e}")
    Errors.Error(str(e), "1")

running = True
mouse_click = (0, 0)
while running:
    #Get events
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = event.pos
    
    main_menues.main_menue(screen, events, mouse_click)
    
    pygame.display.flip()  
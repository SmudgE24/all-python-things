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
import OrbitTerminal
import OrbitLoad
import OrbitSentinel
import OrbitTransferUI
import OrbitScheduler

print("TEST")

# ============================================================
# START UP
# ============================================================

try:
    screen = Orbit_open.start(
        Orbit_open.lines
    )

except Exception as e:

    print(
        f"Opening Error: {e}"
    )

    Errors.Error(
        str(e),
        "1"
    )

# ============================================================
# MAIN LOOP
# ============================================================

running = True
mouse_click = (-10000, -10000)

while running:
    mouse_click = (-10000, -10000)
    events = pygame.event.get()

    for event in events:

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = event.pos

    output = main_menues.main_menue(
        screen,
        events,
        mouse_click
    )

    # ========================================================
    # TERMINAL
    # ========================================================

    if output == "terminal_launch":

        OrbitLoad.run()

        OrbitTerminal.ALL_POWERFUL()

        output = "none"

        OrbitLoad.run()
    
    elif output == "sentinel_launch":

        OrbitLoad.run()
        
        OrbitSentinel.ALL_POWERFULL()

        output = "none"
    
        OrbitLoad.run()

    elif output == "transfer_launch":

        OrbitLoad.run()

        a = OrbitTransferUI.OrbitTransferUI()

        a.run()

        output = "none"

        OrbitLoad.run()

    elif output == "scheduler_launch":
    
            OrbitLoad.run()
    
            a = OrbitScheduler.open_ui()
    
            output = "none"
    
            OrbitLoad.run()
    
    pygame.display.flip()

pygame.quit()
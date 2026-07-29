#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 17:45:52 2026

@author: ethanbrown
"""

import pygame
import drawing

pygame.init()

# -----------------------------
# Window
# -----------------------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Textbox Test")

clock = pygame.time.Clock()

# -----------------------------
# Main
# -----------------------------
textbox_text = ""
textbox_active = False
submitted = False
running = True
while running:

    mouse_click = None
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = event.pos

    screen.fill((35, 35, 35))

    a = drawing.draw_and_type_textbox(
        screen,
        200, 280,           # x, y
        400, 40,            # width, height
        textbox_text,
        textbox_active,
        (255, 255, 255),    # textbox colour
        events,
        mouse_click
    )
    textbox_text = a[0]
    textbox_active = a[1]
    submitted = a[2]
    if submitted:
        print(textbox_text)
        textbox_text = ''

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
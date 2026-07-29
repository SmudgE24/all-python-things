#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 13:34:19 2026

@author: ethanbrown
"""
import pygame

#pygame.draw.rect(screen, (255, 0, 0), (x, y, w, h))
def draw_and_click_button(screen, x, y, w, h, text, color, mouse_click=None):
    pygame.draw.rect(screen, color, (x, y, w, h))
    if mouse_click[0] > x and mouse_click[0] < (x + w) and mouse_click[1] > y and mouse_click[1] < (y + h):
        return True
    else:
        return False

def draw_line(screen, color:tuple, point_1:tuple, point_2:tuple, width:int):
    pygame.draw.line(screen, (0, 0, 255), point_1, point_2, width)

def text_blit(screen, color:tuple, size, text:str, x, y):
    font = pygame.font.SysFont(None, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

def draw_and_type_textbox(screen, x, y, w, h, text, active, color, events, mouse_click=None):
    submitted = False
    font = pygame.font.SysFont("couriernew", 28)

    # Draw textbox
    pygame.draw.rect(screen, color, (x, y, w, h))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, w, h), 2)

    # Activate/deactivate
    if mouse_click is not None:
        if x < mouse_click[0] < x + w and y < mouse_click[1] < y + h:
            active = True
        else:
            active = False

    # Typing
    if active:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]

                elif event.key == pygame.K_RETURN:
                    submitted = True      # Return the current text
                    active = False

                else:
                    text += event.unicode

    # Scroll text if it's too long
    display_text = text
    while font.size(display_text)[0] > w - 10 and len(display_text) > 0:
        display_text = display_text[1:]

    # Draw visible text
    text_surface = font.render(display_text, True, (0, 0, 0))
    screen.blit(text_surface, (x + 5, y + (h - text_surface.get_height()) // 2))

    return [text, active, submitted]
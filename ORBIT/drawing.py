#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 13:34:19 2026

@author: ethanbrown
"""
import pygame

#pygame.draw.rect(screen, (255, 0, 0), (x, y, w, h))
def draw_and_click_button(
    screen,
    x,
    y,
    text,
    text_size,
    text_color,
    color,
    mouse_click=None
):
    font = pygame.font.SysFont(
        "couriernew",
        text_size,
        bold=True
    )
    text_surface = font.render(
        text,
        True,
        text_color
    )
    text_rect = text_surface.get_rect()
    # Padding around the text
    padding_x = 25
    padding_y = 14
    w = text_rect.width + padding_x * 2
    h = text_rect.height + padding_y * 2
    # x and y are the CENTER of the button
    button_rect = pygame.Rect(
        x - w // 2,
        y - h // 2,
        w,
        h
    )
    # Mouse position for hover effect
    mouse_pos = pygame.mouse.get_pos()
    hovered = button_rect.collidepoint(
        mouse_pos
    )
    # --------------------------------------------------------
    # SHADOW
    # --------------------------------------------------------
    shadow_rect = button_rect.copy()
    shadow_rect.y += 5
    pygame.draw.rect(
        screen,
        (30, 30, 30),
        shadow_rect,
        border_radius=12
    )
    # --------------------------------------------------------
    # BUTTON
    # --------------------------------------------------------
    if hovered:
        button_color = tuple(
            min(255, c + 25)
            for c in color
        )
    else:
        button_color = color
    pygame.draw.rect(
        screen,
        button_color,
        button_rect,
        border_radius=12
    )
    # --------------------------------------------------------
    # BORDER
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        button_rect,
        width=2,
        border_radius=12
    )

    # --------------------------------------------------------
    # TEXT
    # --------------------------------------------------------

    text_rect.center = button_rect.center

    screen.blit(
        text_surface,
        text_rect
    )

    # --------------------------------------------------------
    # CLICK
    # --------------------------------------------------------

    if mouse_click is not None:

        if button_rect.collidepoint(
            mouse_click
        ):

            return True

    return False

def draw_line(screen, color:tuple, point_1:tuple, point_2:tuple, width:int):
    pygame.draw.line(screen, color, point_1, point_2, width)

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
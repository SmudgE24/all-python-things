#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:24:46 2026

@author: ethanbrown
"""
import pygame
import drawing

def main_menue(screen, events, mouse_click):
    width, height = screen.get_size()
    drawing.draw_line(screen, (255, 255, 255), (-5, (height // 10)), ((width + 5), (height // 10)), 5)
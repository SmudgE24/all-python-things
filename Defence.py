#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 08:19:24 2026

@author: ethanbrown
"""
import pygame
import random

#Thalkarath
def start():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((900, 945))
    pygame.display.set_caption("Sandbox")
    return screen

class game:
    def __init__(self):
        print("testing - SandBox")
        self.wells = []
        self.Market_image = pygame.transform.scale(pygame.image.load("market.png"), (45, 45))
        self.Well_image = pygame.transform.scale(pygame.image.load("well.jpg"), (45, 45))
        self.School_image = pygame.transform.scale(pygame.image.load("school.png"), (45, 45))
    def run(self):
        lightGreen = (70, 235, 52)
        screen = start()
        to_add = [("well", 0, 7), ("house", 0, 6)]
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    print(mouse_pos)
                    coOrdinites = (int((mouse_pos[0] - (mouse_pos[0] % 45)) / 45), int((mouse_pos[1] - (mouse_pos[1] % 45)) / 45))
                    print(coOrdinites)
                    for i in range(len(to_add)):
                        if to_add[i][1] == coOrdinites[0] and to_add[i][2] == coOrdinites[1]:
                            #menu 4 object
                            print("Menu")
                    
            screen.fill(lightGreen)
            self.screenSetup(screen)
            
            for i in range(len(to_add)):
                if to_add[i][0] == "market":
                    self.marketPlace(screen, to_add[i][1], to_add[i][2])
                elif to_add[i][0] == "house":
                    self.housePlace(screen, to_add[i][1], to_add[i][2])
                elif to_add[i][0] == "well":
                    self.wellPlace(screen, to_add[i][1], to_add[i][2])
                    
            pygame.display.flip()
        pygame.quit()
        
    def screenSetup(self, screen):
        for j in range(20):
            for i in range(20):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(screen, (11, 130, 3), (i*45, j*45, 45, 45))
                else:
                    pygame.draw.rect(screen, (70, 235, 52), (i*45, j*45, 45, 45))
                    
    def check(self, to_add):
        # To Be Finnished Later
        for i in range(len(to_add)):
            if to_add[i][0] == "house":
                house = to_add[i]
    
                for j in range(len(to_add)):
                    if to_add[j][0] == "well":
                        well = to_add[j]
    
                        for x in range(-5, 6):
                            for y in range(-5, 6):
                                point = (house[1] + x, house[2] + y)
    
                                if well[1] == point[0] and well[2] == point[1]:
                                    return True
        return False
    
    def marketPlace(self, screen, x, y):
        screen.blit(self.Market_image, (x*45, y*45))
        
    def housePlace(self, screen, x, y):
        a = (x + y) % 2
        if a == 0:
            House_image = pygame.image.load("house1.jpg")
        else:
            House_image = pygame.image.load("house2.jpg")
        House_image = pygame.transform.scale(House_image, (45, 45))
        screen.blit(House_image, (x*45, y*45))
        
    def wellPlace(self, screen, x, y):
        screen.blit(self.Well_image, (x*45, y*45))
    
    def schoolPlace(self, screen, x, y):
        screen.blit(self.School_image, (x*45, y*45))
        
    def House_menu(self, screen, add):
        x = add[1]
        y = add[2]
        a = (x + y) % 2
        if a == 0:
            House_image = pygame.image.load("house1.jpg")
        else:
            House_image = pygame.image.load("house2.jpg")
        House_image = pygame.transform.scale(House_image, (45, 45))
        if x > 10:
            pygame.draw.rect(screen, (70, 235, 52), (i*45, j*45, 45, 45))
            screen.blit(House_image, (x*45, y*45))
g = game()
g.run()

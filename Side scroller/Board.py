#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:25:27 2026

@author: ethanbrown
"""
import Enemies
import random
random.seed() 
class board:
    def __init__(self, level):
        self.level = level
        self.airs = []
        self.blocks = []
        self.lavas = []
        self.fires = []
        self.chests = []
        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == '.':
                    self.airs.append((j, i))
                elif level[i][j] == 'B':
                    self.blocks.append((j, i))
                elif level[i][j] == 'L':
                    self.lavas.append((j, i))
                elif level[i][j] == 'F':
                    self.fires.append((j, i))
                elif level[i][j] == 'H':
                    self.chests.append((j, i))
    
    def find_chest_contents(self):
        items = ["10 Coins", "Jump boots", "Bow", "+1 life", "Void boots", "Shield +1", "Armour +1", "Armour +2", "Bomb", "Bottle o' healin", "Sword +3", "Key", "Time Freeze 15s", "Flame Gun", "Orb of power +5", "Dagger +1"]
        raraty = [60, 15, 10, 1, 2, 8, 7, 5, 20, 7, 12, 1, 3, 4, 1, 10]
        sum_of = 0
        for i in range(len(raraty)):
            sum_of += raraty[i]
            
        pickednumber1 = random.randint(0, sum_of)
        pickednumber2 = random.randint(0, sum_of)
        two = []
        for number in [pickednumber1, pickednumber2]:
            current_weight = 0
            for iteration in range(len(raraty)):
                current_weight += raraty[iteration]
                if number <= current_weight:
                    two.append(items[iteration])
                    break
        print(two)
    
    def findPoint(self, point):
        level = self.level
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == point:
                    return (x*40, y*40)
        raise Exception("No point")
    
    def setPoint(self, x, y, tile):
        self.level[y][x] = tile
    
    def spawn(self):
        spawns = []
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if self.level[y][x] == "N":
                    a = Enemies.Enemy(level=self.level)
                    a.x = x *40
                    a.y = y * 40
                    spawns.append(a)
        return spawns
    
    def getPlayerBlocks(self, x, y):
        left = x // 40
        right = (x + 39) // 40
        top = y // 40
        bottom = (y + 39) // 40
    
        blocks = []
    
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                blocks.append((x, y))
        
        return blocks
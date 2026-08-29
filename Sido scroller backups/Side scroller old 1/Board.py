#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:25:27 2026

@author: ethanbrown
"""
import Enemies
import Items
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
        """Generate random chest contents from the item database"""
        item_names = list(Items.ITEMS_DB.keys())
        rarities = [Items.ITEMS_DB[name].get("rarity", "common") for name in item_names]
        
        # Weight items by rarity (common=60, uncommon=30, rare=10, very rare=1)
        rarity_weights = {"common": 60, "uncommon": 30, "rare": 10, "very rare": 1}
        weights = [rarity_weights.get(r, 10) for r in rarities]
        
        total_weight = sum(weights)
        
        # Pick 2 random items
        two_items = []
        for _ in range(2):
            pick = random.randint(0, total_weight)
            current_weight = 0
            for i, weight in enumerate(weights):
                current_weight += weight
                if pick <= current_weight:
                    two_items.append(item_names[i])
                    break
        
        print(f"Chest contents: {two_items}")
        return two_items
    
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
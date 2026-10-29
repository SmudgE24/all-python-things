#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:25:27 2026

@author: ethanbrown
"""
from sympy import python

import Enemies
import Items
import random
import bosses
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
                elif level[i][j] == 'F':
                    self.fires.append((j, i))
                elif level[i][j] == 'H':
                    self.chests.append((j, i))
        self.rarity_weights = {"common": 60, "uncommon": 30, "rare": 10, "very rare": 1}
    
    def find_chest_contents(self):
        """Generate random chest contents from the item database"""
        item_names = list(Items.ITEMS_DB.keys())
        rarities = [Items.ITEMS_DB[name].get("rarity", "common") for name in item_names]
        
        # Weight items by rarity (common=60, uncommon=30, rare=10, very rare=1)
        
        weights = [self.rarity_weights.get(r, 10) for r in rarities]
        
        total_weight = sum(weights)
        
        # Pick 2 random items
        two_items = []
        for _ in range(2):
            pick = random.randrange(total_weight)
            current_weight = 0
            for i, weight in enumerate(weights):
                current_weight += weight
                if pick < current_weight:
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

    def BossSpawn(self):
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if self.level[y][x] == "X":
                    a = bosses.fire_boss(level=self.level)
                    a.x = x *40
                    a.y = y * 40 - (a.hight - 40)
                    return a
        return None
    
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

    def lava_drain(self):
        direc = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if self.level[y][x] == "D":
                    for i in range(len(direc)):
                        dx, dy = direc[i]
                        nx, ny = x + dx, y + dy
                        if 0 <= ny < len(self.level) and 0 <= nx < len(self.level[ny]):
                            if str(self.level[ny][nx]).startswith("L"):
                                self.level[ny][nx] = "."
        return self.level


    def lava_tick(self):
        old_level = [row[:] for row in self.level]

        amounts = [
            [int(str(tile)[1:]) if str(tile).startswith("L") else 0 for tile in row]
            for row in old_level
        ]

        moved_down = [[0] * len(row) for row in old_level]
        received_down = [[0] * len(row) for row in old_level]

        # Gravity: process from bottom to top
        for y in range(len(old_level) - 1, -1, -1):
            for x, tile in enumerate(old_level[y]):
                if not str(tile).startswith("L"):
                    continue

                if y + 1 >= len(old_level):
                    continue

                if x >= len(old_level[y + 1]):
                    continue

                below = old_level[y + 1][x]

                if below in ("B", "C", "H", "L7"):
                    continue

                # Account for space created by lava moving down from this cell
                capacity = (
                    7
                    - amounts[y + 1][x]
                    + moved_down[y + 1][x]
                    - received_down[y + 1][x]
                )

                moved = min(amounts[y][x], max(0, capacity))

                moved_down[y][x] = moved
                received_down[y + 1][x] += moved

        # Apply gravity together
        next_amounts = [
            [
                amounts[y][x] - moved_down[y][x] + received_down[y][x]
                for x in range(len(old_level[y]))
            ]
            for y in range(len(old_level))
        ]

        # Horizontal equalisation
        # Each transfer moves one unit from a fuller cell to a lower cell
        for y, row in enumerate(old_level):
            for x in range(len(row) - 1):
                left_tile = row[x]
                right_tile = row[x + 1]

                # Only lava and empty spaces can contain lava
                if left_tile != "." and not str(left_tile).startswith("L"):
                    continue

                if right_tile != "." and not str(right_tile).startswith("L"):
                    continue

                left_amount = next_amounts[y][x]
                right_amount = next_amounts[y][x + 1]

                # A difference of 0 or 1 is already approximately equal
                if abs(left_amount - right_amount) < 2:
                    continue

                # Find the fuller cell and the lower cell
                if left_amount > right_amount:
                    source_x = x
                    target_x = x + 1
                else:
                    source_x = x + 1
                    target_x = x

                # Only lava that was already present can spread sideways
                if not str(row[source_x]).startswith("L"):
                    continue

                # Lava that moved down this tick cannot also spread sideways
                if moved_down[y][source_x] > 0:
                    continue

                # Lava only spreads sideways when blocked below
                if y + 1 < len(old_level):
                    if source_x < len(old_level[y + 1]):
                        below = old_level[y + 1][source_x]

                        if below not in ("B", "C", "H", "L7"):
                            continue

                # Transfer exactly one unit, preserving the L7 maximum
                if (
                    next_amounts[y][source_x] > 0
                    and next_amounts[y][target_x] < 7
                    and next_amounts[y][source_x]
                        - next_amounts[y][target_x] >= 2
                ):
                    next_amounts[y][source_x] -= 1
                    next_amounts[y][target_x] += 1

        # Write the new lava levels back into the map
        for y, row in enumerate(old_level):
            for x, tile in enumerate(row):
                amount = next_amounts[y][x]

                if str(tile).startswith("L") or amount > 0:
                    if amount <= 0:
                        self.level[y][x] = "."
                    else:
                        self.level[y][x] = "L" + str(amount)

        return self.level

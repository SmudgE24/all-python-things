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
            [int(tile[1:]) if str(tile).startswith("L") else 0 for tile in row]
            for row in old_level
        ]
        moved_down = [[0] * len(row) for row in old_level]
        received_down = [[0] * len(row) for row in old_level]

        # Resolve gravity using the snapshot, so falling lava cannot fall again
        # during this tick. Bottom-up capacity accounting prevents overfilling.
        for y in range(len(old_level) - 1, -1, -1):
            for x, tile in enumerate(old_level[y]):
                if not str(tile).startswith("L") or y + 1 >= len(old_level):
                    continue

                below = old_level[y + 1][x] if x < len(old_level[y + 1]) else None
                if below is None or below in ("B", "C", "H", "L7"):
                    continue

                below_amount = amounts[y + 1][x]
                capacity = 7 - below_amount + moved_down[y + 1][x] - received_down[y + 1][x]
                moved = min(amounts[y][x], max(0, capacity))
                moved_down[y][x] = moved
                received_down[y + 1][x] = moved

        next_amounts = [row[:] for row in amounts]
        for y, row in enumerate(old_level):
            for x, tile in enumerate(row):
                if str(tile).startswith("L"):
                    next_amounts[y][x] -= moved_down[y][x]
                    if y + 1 < len(old_level) and x < len(old_level[y + 1]):
                        next_amounts[y + 1][x] += received_down[y + 1][x]

        # Horizontal transfers are also decided from the snapshot and applied
        # together, allowing every lava cell to move on the same tick.
        lateral_moves = []
        for y, row in enumerate(old_level):
            for x, tile in enumerate(row):
                if not str(tile).startswith("L") or moved_down[y][x]:
                    continue
                if y + 1 < len(old_level):
                    below = old_level[y + 1][x] if x < len(old_level[y + 1]) else None
                    if below is not None and below not in ("B", "C", "H", "L7"):
                        continue

                for neighbor_x in (x + 1, x - 1):
                    if not 0 <= neighbor_x < len(row):
                        continue
                    neighbor = old_level[y][neighbor_x]
                    if neighbor == "." or (
                        str(neighbor).startswith("L")
                        and amounts[y][neighbor_x] < amounts[y][x] - 1
                    ):
                        lateral_moves.append((y, x, neighbor_x))

        lateral_out = [[0] * len(row) for row in old_level]
        lateral_in = [[0] * len(row) for row in old_level]
        for y, source_x, target_x in lateral_moves:
            target_capacity = (
                7 - next_amounts[y][target_x] + lateral_out[y][target_x]
            )
            if (
                lateral_out[y][source_x] < amounts[y][source_x]
                and lateral_in[y][target_x] < target_capacity
            ):
                lateral_out[y][source_x] += 1
                lateral_in[y][target_x] += 1

        for y, row in enumerate(old_level):
            for x, tile in enumerate(row):
                next_amounts[y][x] += lateral_in[y][x] - lateral_out[y][x]

        for y, row in enumerate(old_level):
            for x, tile in enumerate(row):
                if str(tile).startswith("L") or next_amounts[y][x]:
                    self.level[y][x] = "L" + str(next_amounts[y][x])

        for y, row in enumerate(self.level):
            for x, tile in enumerate(row):
                if tile == "L0":
                    self.level[y][x] = "."
        return self.level

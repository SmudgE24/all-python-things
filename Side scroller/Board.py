#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:25:27 2026

@author: ethanbrown
"""
import Enemies
import Items
import random
import bosses
import Player
random.seed() 
class board:
    def __init__(self, level):
        self.smoke_list = []
        self.ticks = 0
        self.ticks = 0
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
    
    def spawn(self, levelNo=None):
        a = Enemies.Enemy(level=self.level)
        if levelNo is not None and levelNo > 6:
            if levelNo < 26:
                a.probs["spider"] = 0.1 + (0.005 * levelNo)
                a.probs["wolf"] = 0.5 - (0.005 * levelNo)
            else:
                a.probs["spider"] = 0.3
                a.probs["wolf"] = 0.3
        spawns = []
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if self.level[y][x] == "N":
                    a_type = random.choices(list(a.probs.keys()), weights=list(a.probs.values()))[0]
                    if a_type == 'bat':
                        new = Enemies.bat(level=self.level)
                    elif a_type == 'wolf':
                        new = Enemies.wolf(level=self.level)
                    elif a_type == 'spider':
                        new = Enemies.spider(level=self.level)
                    new.probs = a.probs.copy()
                    new.x = x *40
                    new.y = y * 40
                    spawns.append(new)
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

    def smoke(self):
        to_pop = []
        for i in range(len(self.smoke_list)):
            self.smoke_list[i].time += 1
            if self.smoke_list[i].time > 400:
                to_pop.append(i)

            else:
                answer = self.smoke_list[i].is_under_wall('B', True)
                if not answer:
                    self.smoke_list[i].y -= 1
                else:
                    if not self.smoke_list[i].is_touching_wall_left('B', True):
                        self.smoke_list[i].x -= 1
                    elif not self.smoke_list[i].is_touching_wall_right('B', True):
                        self.smoke_list[i].x += 1
                    else:
                        to_pop.append(i)

        for i in range(len(to_pop)):
            self.smoke_list.pop(len(to_pop) - 1 - i)

        return self.smoke_list
            
    def sulpher(self):
        self.ticks += 1
        if self.ticks % 280 == 30:
            for y in range(len(self.level)):
                for x in range(len(self.level[y])):
                    if self.level[y][x] == "M":
                        new_smoke_list = movable_entity('smoke', (145, 145, 145), self.level)
                        new_smoke_list.x = x * 40
                        new_smoke_list.y = y * 40
                        self.smoke_list.append(new_smoke_list)

        return self.smoke()




    def lava_drain(self):
        if self.ticks % 600 == 10:
            for y in range(len(self.level)):
                for x in range(len(self.level[y])):
                    if self.level[y][x] == "D":
                        self.level[y + 1][x] = "L1"
        return self.level

    def water_drain(self):
        # Spawns a full block of water (W14) from ceiling drippers 'w'
        if self.ticks % 450 == 10:
            for y in range(len(self.level)):
                for x in range(len(self.level[y])):
                    if self.level[y][x] == "w":
                        if y + 1 < len(self.level) and self.level[y + 1][x] == ".":
                            self.level[y + 1][x] = "W14"
        return self.level


    def water_tick(self):
        old_level = [row[:] for row in self.level]

        height = len(old_level)

        amounts = [
            [int(tile[1:]) if tile.startswith("W") else 0 for tile in row]
            for row in old_level
        ]

        moved_down = [[0] * len(row) for row in old_level]
        received_down = [[0] * len(row) for row in old_level]

        # Gravity processing: bottom to top
        for y in range(height - 1, -1, -1):
            row = old_level[y]

            for x, tile in enumerate(row):
                if not tile.startswith("W"):
                    continue

                if y + 1 >= height or x >= len(old_level[y + 1]):
                    continue

                below = old_level[y + 1][x]

                if below in ("B", "C", "H", "W14", "L7", "K"):
                    continue

                capacity = (
                    14
                    - amounts[y + 1][x]
                    + moved_down[y + 1][x]
                    - received_down[y + 1][x]
                )

                moved = min(amounts[y][x], max(0, capacity))

                moved_down[y][x] = moved
                received_down[y + 1][x] += moved

        # Apply gravity directly to amounts
        for y, row in enumerate(amounts):
            for x in range(len(row)):
                row[x] = row[x] - moved_down[y][x] + received_down[y][x]

        # Horizontal equalisation
        for y, row in enumerate(old_level):
            amount_row = amounts[y]
            moved_row = moved_down[y]

            for x in range(len(row) - 1):
                left_tile = row[x]
                right_tile = row[x + 1]

                if left_tile != "." and not left_tile.startswith("W"):
                    continue

                if right_tile != "." and not right_tile.startswith("W"):
                    continue

                left_amount = amount_row[x]
                right_amount = amount_row[x + 1]

                if abs(left_amount - right_amount) < 2:
                    continue

                if left_amount > right_amount:
                    source_x, target_x = x, x + 1
                else:
                    source_x, target_x = x + 1, x

                if not row[source_x].startswith("W") or moved_row[source_x] > 0:
                    continue

                if y + 1 < height and source_x < len(old_level[y + 1]):
                    if old_level[y + 1][source_x] not in ("B", "C", "H", "W14", "u", "b"):
                        continue

                if amount_row[source_x] > 0 and amount_row[target_x] < 14:
                    amount_row[source_x] -= 1
                    amount_row[target_x] += 1

        # Write the new water levels back
        for y, row in enumerate(old_level):
            for x, tile in enumerate(row):
                amount = amounts[y][x]

                if tile.startswith("W") or amount > 0:
                    self.level[y][x] = "." if amount <= 0 else "W" + str(amount)

        return self.level



    def lava_tick(self):
        old_level = [row[:] for row in self.level]

        height = len(old_level)

        amounts = [
            [int(tile[1:]) if tile.startswith("L") else 0 for tile in row]
            for row in old_level
        ]

        moved_down = [[0] * len(row) for row in old_level]
        received_down = [[0] * len(row) for row in old_level]

        # Gravity: process from bottom to top
        for y in range(height - 1, -1, -1):
            row = old_level[y]

            for x, tile in enumerate(row):
                if not tile.startswith("L"):
                    continue

                if y + 1 >= height or x >= len(old_level[y + 1]):
                    continue

                below = old_level[y + 1][x]

                if below in ("B", "C", "H", "L7", "K", "u", "b"):
                    continue

                capacity = (
                    7
                    - amounts[y + 1][x]
                    + moved_down[y + 1][x]
                    - received_down[y + 1][x]
                )

                moved = min(amounts[y][x], max(0, capacity))

                moved_down[y][x] = moved
                received_down[y + 1][x] += moved

        # Apply gravity directly to amounts
        for y, row in enumerate(amounts):
            for x in range(len(row)):
                row[x] = row[x] - moved_down[y][x] + received_down[y][x]

        # Horizontal equalisation
        for y, row in enumerate(old_level):
            amount_row = amounts[y]
            moved_row = moved_down[y]

            for x in range(len(row) - 1):
                left_tile = row[x]
                right_tile = row[x + 1]

                if left_tile != "." and not left_tile.startswith("L"):
                    continue

                if right_tile != "." and not right_tile.startswith("L"):
                    continue

                left_amount = amount_row[x]
                right_amount = amount_row[x + 1]

                if abs(left_amount - right_amount) < 2:
                    continue

                if left_amount > right_amount:
                    source_x, target_x = x, x + 1
                else:
                    source_x, target_x = x + 1, x

                if not row[source_x].startswith("L"):
                    continue

                if moved_row[source_x] > 0:
                    continue

                if y + 1 < height and source_x < len(old_level[y + 1]):
                    below = old_level[y + 1][source_x]

                    if below not in ("B", "C", "H", "L7", "K"):
                        continue

                if (
                    amount_row[source_x] > 0
                    and amount_row[target_x] < 7
                    and amount_row[source_x] - amount_row[target_x] >= 2
                ):
                    amount_row[source_x] -= 1
                    amount_row[target_x] += 1

        # Write the new lava levels back
        for y, row in enumerate(old_level):
            for x, tile in enumerate(row):
                amount = amounts[y][x]

                if tile.startswith("L") or amount > 0:
                    self.level[y][x] = "." if amount <= 0 else "L" + str(amount)

        return self.level




class movable_entity(Player.player):
    def __init__(self, name, color, level):
        self.time = 0
        self.name = name
        self.x = 0
        self.y = 0
        self.color = color
        self.jumpmax = 0
        self.hp = 1
        Player.player.__init__(self, level, self.jumpmax, self.hp)

    def isTouchingPlayer(self, player):
            if (
                player.x < self.x + 40 and
                player.x + player.width > self.x and
                player.y < self.y + 40 and
                player.y + player.hight > self.y
            ):
                if player.vy > 0 and player.last_y + player.hight <= self.y + 5:
                    return True
                else:
                    return True
            
            return False
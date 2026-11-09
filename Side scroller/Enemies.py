#!/usr/bin/env python3
"""
Created on Thu Jul 2 18:17:20 2026
@author: ethanbrown
"""
import random
import Player
class Enemy(Player.player):
    def __init__(self, level):
        self.probs = {
            "wolf": 0.6,
            "bat": 0.4,}
        self.level = level
        self.speed = random.randint(1, 3)
        self.area = random.randint(2, 5) * 40
        self.jumpmax = 0
        self.hp = 1
        self.x = 0
        self.y = 0
        self.last_x = self.x
        self.last_y = self.y
        Player.player.__init__(self, level, self.jumpmax, self.hp)
    def isTouchingPlayer(self, player):
        if (
            player.x < self.x + 40 and
            player.x + player.width > self.x and
            player.y < self.y + 40 and
            player.y + player.hight > self.y
        ):
            if player.vy > 0 and player.last_y + player.hight <= self.y + 5:
                return "stomp"
            else:
                return "hit"
        return None
    def move(self, ticks, Player):
        def lava():
            cngol = True
            cngor = True
            try:
                if list(self.level[(self.y + 55) // 40][self.x // 40])[0] == 'L' or list(self.level[(self.y + 55) // 40][self.x // 40])[0] == '.':
                    cngol = False
                elif list(self.level[(self.y + 55) // 40][(self.x + 55) // 40])[0] == 'L' or list(self.level[(self.y + 55) // 40][(self.x + 55) // 40])[0] == '.':
                    cngor = False
            except IndexError:
                pass
            return (cngol, cngor)

        if ticks % self.area < self.area / 2:
            left = True
            right = False
        else:
            left = False
            right = True
        block = "B"
        Or = True
        if left:
            if not self.is_touching_wall_left(block, Or):
                for i in range(self.speed):
                    if not self.is_touching_wall_left(block, Or) and lava()[0]:
                        self.x -= 1
                        self.going_left = True
                    else:
                        pass
        
        if right:
            if not self.is_touching_wall_right(block, Or):
                for i in range(self.speed):
                    if not self.is_touching_wall_right(block, Or) and lava()[1]:
                        self.x += 1
                        self.going_left = False
                    else:
                        pass
        

class NPC(Enemy):
    def __init__(self, level, name, dialogue_lines):
        Enemy.__init__(self, level)
        self.name = name
        self.dialogue = dialogue_lines # A list of strings: ["Hello Genghis.", "Beware the caves..."]
        self.hp = 999 # Immortal peaceful NPC
        self.speed = 0
    def is_near_player(self, player):
        # Checks if player is within 60 pixels (~1.5 tiles) horizontally and vertically
        return abs(player.x - self.x) < 60 and abs(player.y - self.y) < 60
    def move(self, ticks, Player):
        pass # NPCs stay completely stationary

class wolf(Enemy):
    def __init__(self, level):
        Enemy.__init__(self, level)
        self.hp = 3
        self.jumpmax = 1

class bat(Enemy):
    def __init__(self, level):
        Enemy.__init__(self, level)
        self.hp = 1
        self.jumpmax = 1
    def move(self, ticks, Player):
        vector = [0, 0]
        if Player.y < self.y:
            vector[1] += 5
        elif Player.y > self.y:
            vector[1] -= 5
        if Player.x < self.x:
            vector[0] += 5
        elif Player.x > self.x:
            vector[0] -= 5
        if not self.is_under_wall('B', True) and vector[1] < 0:
            self.y += vector[1]
        elif not self.is_on_wall('B', True) and vector[1] > 0:
            self.y += vector[1]
        if not self.is_touching_wall_right('B', True) and vector[0] > 0:
            self.x += vector[0]
        elif not self.is_touching_wall_left('B', True) and vector[0] < 0:
            self.y += vector[0]
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
            "bat": 0.4,
            "spider": 0.0,}
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
        self.hp = 242424 # Immortal peaceful NPC
        self.speed = 0
        self.isinvicinity = False
        self.text_current = None
        self.wasinvicinity = False
    def is_near_player(self, player):
        if self.isinvicinity:
            self.wasinvicinity = True
        else:
            self.wasinvicinity = False
        # Checks if player is within 60 pixels (~1.5 tiles) horizontally and vertically
        if abs(player.x - self.x) < 60 and abs(player.y - self.y) < 60:
            self.isinvicinity = True
        else:
            self.isinvicinity = False
        return abs(player.x - self.x) < 60 and abs(player.y - self.y) < 60
    def move(self, ticks, Player):
        pass # NPCs stay completely stationary
    def text(self):
        if self.isinvicinity and not self.wasinvicinity:
            self.text_current = f"{self.name}:  {random.choice(self.dialogue)}"
        return self.text_current
    def next_line(self):
        self.text_current = f"{self.name}:  {random.choice(self.dialogue)}"

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
        speed = 1 

        # 1. Determine direction (Corrected for standard 2D coordinates)
        if Player.y < self.y:
            vector[1] -= speed  # Move UP
        elif Player.y > self.y:
            vector[1] += speed  # Move DOWN

        if Player.x < self.x:
            vector[0] -= speed  # Move LEFT
            self.going_left
        elif Player.x > self.x:
            vector[0] += speed  # Move RIGHT
            self.going_left = False

        
        if vector[1] < 0 and not self.is_under_wall('B', True):
            self.y += vector[1]
        elif vector[1] > 0 and not self.is_on_wall('B', True):
            self.y += vector[1]

        
        if vector[0] > 0 and not self.is_touching_wall_right('B', True):
            self.x += vector[0]
        elif vector[0] < 0 and not self.is_touching_wall_left('B', True):
            self.x += vector[0]  # Fixed: changed self.y to self.x

    def update_vy(self):
        self.vy = 0

class spider(Enemy):
    def __init__(self, level):
        Enemy.__init__(self, level)
        self.hp = 1
        self.jumpmax = 1
        self.in_spider_web = False
    
    def move_on_web(self, ticks, Player):
        vector = [0, 0]
        speed = 5

        # 1. Determine direction (Corrected for standard 2D coordinates)
        if Player.y < self.y:
            vector[1] -= speed  # Move UP
        elif Player.y > self.y:
            vector[1] += speed  # Move DOWN

        if Player.x < self.x:
            vector[0] -= speed  # Move LEFT
            self.going_left
        elif Player.x > self.x:
            vector[0] += speed  # Move RIGHT
            self.going_left = False

        
        if vector[1] < 0 and not self.is_under_wall('B', True):
            self.y += vector[1]
        elif vector[1] > 0 and not self.is_on_wall('B', True):
            self.y += vector[1]

        
        if vector[0] > 0 and not self.is_touching_wall_right('B', True):
            self.x += vector[0]
        elif vector[0] < 0 and not self.is_touching_wall_left('B', True):
            self.x += vector[0]  # Fixed: changed self.y to self.x

    def move(self, ticks, Player):
        player = Player
        self.speed = 4
        if self.is_on_wall("u", True):
            self.in_spider_web = True
        else:
            self.in_spider_web = False

        try:
            if self.speed >= 14:
                self.speed = 13
        except:
            pass
        if self.in_spider_web == False:
            left = False
            right = False
            if player.x + (40 * 10) < self.x:
                left = False
                right = False
            elif player.x + (40 * 10) > self.x and player.x < self.x:
                left = False
                right = True
            elif player.x == self.x:
                left = False
                right = False
            elif player.x - (40 * 10) < self.x and player.x > self.x:
                left = True
                right = False
            else:
                left = False
                right = False
            
            Or = True
            block = "B"
            INVENTORY_WIDTH = 150  # Prevent player from entering inventory area
            MIN_X = INVENTORY_WIDTH / 40  # Convert to block units (40 pixels per block)
            
            if left:
                if not self.is_touching_wall_left(block, Or) or not self.is_touching_wall_left('b', Or):
                    for i in range(self.speed):
                        if not self.is_touching_wall_left(block, Or):
                            self.x -= 1
                        else:
                            pass
                self.going_left = True

            if right:
                if not self.is_touching_wall_right(block, Or) or not self.is_touching_wall_right('b', Or):
                    for i in range(self.speed):
                        if not self.is_touching_wall_right(block, Or):
                            self.x += 1
                        else:
                            pass
                self.going_left = False
        if self.in_spider_web:
            self.move_on_web(ticks, player)

        if (ticks / 40) % 20 == 0:
            going = True
            iteration = 0
            while going:
                if self.level[(self.y // 40) + iteration][self.x // 40] == "u":
                    going = True
                    iteration += 1
                else:
                    self.level[(self.y // 40) + iteration][self.x // 40] = "u"
                    going = False
        

    def update_vy(self):
        if self.in_spider_web:
            self.vy = 0
        else:
            Or = True
            block = "B"
                    
            self.vy += self.gravity
            
            if self.vy > 12:
                self.vy = 12
            
            if self.is_on_wall("P", True) == False:
                self.y += self.vy
            else:
                if self.vy > 0:
                    self.vy = 0
                    self.y += self.vy
                    self.jumps = 0
            
            if self.vy > 0:
                if self.is_on_wall(block, Or):
                    while self.is_on_wall(block, Or):
                        self.y -= 1
                    
            elif self.vy < 0:
                if self.is_under_wall(block, Or):
                    while self.is_under_wall(block, Or):
                        self.y += 1
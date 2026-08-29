#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 18:17:20 2026

@author: ethanbrown
"""
import random
import Player
class Enemy(Player.player):
    def __init__(self, level):
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
            player.x + 40 > self.x and
            player.y < self.y + 40 and
            player.y + 40 > self.y
        ):
            if player.vy > 0 and player.last_y + 40 <= self.y + 5:
                return "stomp"
            else:
                return "hit"
    
        return None
    
    def move(self, ticks):
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
                    if not self.is_touching_wall_left(block, Or) or not self.is_touching_wall_left(block="L", Or=True):
                        self.x -= 1
                    else:
                        pass
            self.going_left = True

        if right:
            if not self.is_touching_wall_right(block, Or):
                for i in range(self.speed):
                    if not self.is_touching_wall_right(block, Or) or not self.is_touching_wall_right(block="L", Or=True):
                        self.x += 1
                    else:
                        pass
            self.going_left = False
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 09:34:07 2026

@author: ethanbrown
"""
def pirateMain():
    return weapon((0,0), player_x=(0), player_y=(0), size_width=40, size_hight=7, level=[])

def pirateSuper():
    return weapon((-10,0), player_x=(0), player_y=(0), size_width=40, size_hight=7, level=[])

class weapon:
    def __init__(self, velocity, player_x, player_y, size_width, size_hight, level):
        self.velocity = velocity
        self.x = player_x
        self.y = player_y
        self.size_width = size_width
        self.size_hight = size_hight
        self.level = level
    
    def move(self, moveto_x=None, moveto_y=None):
        if moveto_x is None and moveto_y is None:
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        elif moveto_x is not None and moveto_y is not None:
            self.x = moveto_x
            self.y = moveto_y
        else:
            raise Exception("Please make both moveto_x and moveto_y either integers of both 'None'")
    
    def is_touching_player(self, player_x, player_y):
        if ((self.x > player_x and self.x < (player_x + 40)) and (self.y > player_y and self.y < (player_y + 40))) or (((self.x + self.size_width) > player_x and (self.x + self.size_width) < (player_x + 40)) and ((self.y + self.size_hight) > (self.y + self.size_hight) and self.y < (player_y + 40))):
            return True
        else:
            return False
    
    def touching(self, block):
        if self.level[self.y // 40][self.x // 40] == block:
            return True
        if self.level[(self.y + self.size_hight) // 40][self.x // 40] == block:
            return True
        if self.level[(self.y + self.size_hight) // 40][(self.x + self.size_width) // 40] == block:
            return True
        if self.level[(self.y + self.size_hight) // 40][(self.x + self.size_width) // 40] == block:
            return True
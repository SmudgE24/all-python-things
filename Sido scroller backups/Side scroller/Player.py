#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 18:29:29 2026

@author: ethanbrown
"""

class player:
    def __init__(self, level, jumpmax, hp):
        self.on_fire_for = None
        self.on_fire = False
        self.coins = 0
        self.jumps = 0
        self.going_left = False

        self.vy = 0

        self.x = 0
        self.y = 0

        self.level = level

        self.jumpmax = jumpmax
        self.hp = hp

        self.inventory = []

    def move(self, left, right):
        Or = True
        block = "B"
        if left:
            if not self.is_touching_wall_left(block, Or):
                for i in range(self.speed):
                    if not self.is_touching_wall_left(block, Or):
                        self.x -= 1
                    else:
                        pass
            self.going_left = True

        if right:
            if not self.is_touching_wall_right(block, Or):
                for i in range(self.speed):
                    if not self.is_touching_wall_right(block, Or):
                        self.x += 1
                    else:
                        pass
            self.going_left = False

    def jump(self):
        Or = True
        block = "B"
        self.y += 1
        
        on_ground = self.is_on_wall(block, Or)
        self.y -= 1
        if on_ground:
            self.jumps = 0
        if self.jumps < self.jumpmax:
            self.vy = -12
            self.jumps += 1

    def update_vy(self):
        Or = True
        block = "B"
        self.vy += 1

        if self.vy > 10:
            self.vy = 10

        self.y += self.vy

        if self.vy > 0:
            if self.is_on_wall(block, Or):
                while self.is_on_wall(block, Or):
                    self.y -= 1
        
        elif self.vy < 0:
            if self.is_under_wall(block, Or):
                while self.is_under_wall(block, Or):
                    self.y += 1

    def is_on_wall(self, block, Or):
        left = (self.x + 1) // 40
        right = (self.x + 39) // 40
        bottom = (self.y + 41) // 40
    
        if bottom < 0 or bottom >= len(self.level):
            return False
    
        if left < 0 or right >= len(self.level[0]):
            return False
        
        if Or:
            return (
                self.level[bottom][left] == block or
                self.level[bottom][right] == block
            )
        else:
            return (
                self.level[bottom][left] == block and
                self.level[bottom][right] == block
                )
    
    def is_under_wall(self, block, Or):
        left = (self.x + 1) // 40
        right = (self.x + 39) // 40
        top = ((self.y - 1) // 40)
    
        if top < 0 or top >= len(self.level):
            return False
    
        if left < 0 or right >= len(self.level[0]):
            return False
    
        if Or:
            return (
                self.level[top][left] == block or
                self.level[top][right] == block
            )
        else:
            return (
                self.level[top][left] == block and
                self.level[top][right] == block
                )
    
    
    def is_touching_wall_left(self, block, Or):
        left = (self.x - 1) // 40
        top = ((self.y + 1) // 40)
        bottom = ((self.y + 39) // 40)
    
        if left < 0:
            return True
    
        if top < 0 or bottom >= len(self.level):
            return False
    
        if Or:
            return (
                self.level[top][left] == block or
                self.level[bottom][left] == block
            )
        else:
            return (
                self.level[top][left] == block and
                self.level[bottom][left] == block
                )
    
    def is_touching_wall_right(self, block, Or):
        right = (self.x + 40) // 40
        top = ((self.y + 1) // 40)
        bottom = ((self.y + 39) // 40)
    
        if right >= len(self.level[0]):
            return True
    
        if top < 0 or bottom >= len(self.level):
            return False
    
        if Or:
            return (
                self.level[top][right] == block or
                self.level[bottom][right] == block
            )
        else:
            return (
                self.level[top][right] == block and
                self.level[bottom][right] == block
                )

    def update_board(self, level):
        self.level = level

    def take_damage(self, amount):
        self.hp -= amount

    def death(self):
        if self.hp <= 0:
            return True
        else:
            return False

    def AppendInventory(self, item):
        self.inventory.append(item)

    def Take_item(self, item):
        for i in range(len(self.inventory)):
            if self.inventory[i] == item:
                self.inventory.pop(i)
                break
    
    def FireTick(self, ticks):
        if self.on_fire:
            if ticks % 40 == 0:
                self.take_damage(1)
            if self.on_fire_for is not None:
                self.on_fire_for += 1
            else:
                self.on_fire_for = 1
            
            if self.on_fire_for == 85:
                self.on_fire = False
        if self.is_on_wall(block="L", Or=False):
            self.on_fire = True
            self.on_fire_for = None
    

class Pirate(player):
    def __init__(self, level):
        self.charge_count = 0
        self.super_charged = True
        self.current_attack = None
        self.current_super = None
        # self.attack_type = "sword"
        # self.ability = "dash"
        # self.super = "cannon"
        self.hp = 3
        self.speed = 7
        self.damage = 4
        self.jumpmax = 2
        player.__init__(self, level, self.jumpmax, self.hp)
    
    def attack(self):
        self.current_attack = weapon((0,0), player_x=(self.x+40), player_y=(self.y+40), size_width=40, size_hight=7)
    
    #def use_ability(self):
    
    def super_attack(self):
        if self.super_charged:
            self.super_charged = False
            if self.going_left:
                self.current_super = weapon((-10,0), player_x=(self.x+40), player_y=(self.y+40), size_width=40, size_hight=7)
            else:
                self.current_super = weapon((-10,0), player_x=(self.x+40), player_y=(self.y+40), size_width=40, size_hight=7)
    
    def update_attacks(self, holding_attack, holding_super_attack):
        if not holding_attack:
            self.current_attack = None
        if not holding_super_attack:
            self.current_super = None
        
        if self.current_attack is not None:
            self.current_attack.move(self.x+40, self.y+20)
        if self.current_super is not None:
            self.current_super.move()
    
    def recharge_super(self, coins_gained):
        self.charge_count += coins_gained
        if self.charge_count > 10 and self.super_charged == False:
            self.charge_count -= 10
            self.super_charged = True
    

class weapon:
    def __init__(self, velocity, player_x, player_y, size_width, size_hight):
        self.velocity = velocity
        self.x = player_x
        self.y = player_y
        self.size_width = size_width
        self.size_hight = size_hight
    
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
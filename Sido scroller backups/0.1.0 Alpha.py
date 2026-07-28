#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:17:58 2026

@author: ethanbrownhello
"""
import random
import pygame

B = 'B'
A = '.'
L = 'L'

level = [
    [A, A, A, A, B, A, A],
    [A, A, A, A, B, A, A],
    [B, L, L, B, B, B, B],
    [A, A, A, A, B, A, A],
    [A, A, A, A, A, A, A],
    [A, A, A, A, A, A, A],
]
#tile size = 40 x 40

#Window = 1280 × 720

#player size = 40 x 40

class player:
    def __init__(self, level, jumpmax, hp):
        self.coins = 0
        self.jump_amount = 0
        self.going_left = False

        self.vy = 0

        self.x = 0
        self.y = 0

        self.level = level

        self.jumpmax = jumpmax
        self.hp = hp

        self.inventory = []

    def move(self, left, right):
        if left:
            if not self.is_touching_wall_left():
                self.x -= self.speed
            self.going_left = True

        if right:
            if not self.is_touching_wall_right():
                self.x += self.speed
            self.going_left = False

    def jump(self):
        self.y += 1
        on_ground = self.is_on_wall()
        self.y -= 1
    
        if on_ground:
            self.vy = -10

    def update_vy(self):
        self.vy += 1

        if self.vy > 10:
            self.vy = 10

        self.y += self.vy

        if self.vy > 0:
            if self.is_on_wall():
                while self.is_on_wall():
                    self.y -= 1
                self.vy = 0

        elif self.vy < 0:
            if self.is_under_wall():
                while self.is_under_wall():
                    self.y += 1
                self.vy = 0

    def is_on_wall(self):
        wy = 160
    
        left = (self.x + 1) // 40
        right = (self.x + 39) // 40
        bottom = (self.y + 41 - wy) // 40
    
        print("Player:", self.x, self.y)
        print("Tiles:", left, right, bottom)
    
        if bottom < 0 or bottom >= len(self.level):
            print("Y out of bounds")
            return False
    
        if left < 0 or right >= len(self.level[0]):
            print("X out of bounds")
            return False
    
        print(self.level[bottom][left], self.level[bottom][right])
    
        return (
            self.level[bottom][left] == "B" or
            self.level[bottom][right] == "B"
        )
    
    
    def is_under_wall(self):
        wy = 160
    
        left = (self.x + 1) // 40
        right = (self.x + 39) // 40
        top = ((self.y - 1 - wy) // 40)
    
        if top < 0 or top >= len(self.level):
            return False
    
        if left < 0 or right >= len(self.level[0]):
            return False
    
        return (
            self.level[top][left] == "B" or
            self.level[top][right] == "B"
        )
    
    
    def is_touching_wall_left(self):
        wy = 160
    
        left = (self.x - 1) // 40
        top = ((self.y + 1 - wy) // 40)
        bottom = ((self.y + 39 - wy) // 40)
    
        if left < 0:
            return True
    
        if top < 0 or bottom >= len(self.level):
            return False
    
        return (
            self.level[top][left] == "B" or
            self.level[bottom][left] == "B"
        )
    
    
    def is_touching_wall_right(self):
        wy = 160
    
        right = (self.x + 40) // 40
        top = ((self.y + 1 - wy) // 40)
        bottom = ((self.y + 39 - wy) // 40)
    
        if right >= len(self.level[0]):
            return True
    
        if top < 0 or bottom >= len(self.level):
            return False
    
        return (
            self.level[top][right] == "B" or
            self.level[bottom][right] == "B"
        )

    def update_board(self, level):
        self.level = level

    def take_damage(self, amount):
        self.hp -= amount

    def death(self):
        return self.hp <= 0

    def AppendInventory(self, item):
        self.inventory.append(item)

    def Take_item(self, item):
        for i in range(len(self.inventory)):
            if self.inventory[i] == item:
                self.inventory.pop(i)
                break

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
        self.jumpmax = 1
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
        
    #def 

def start():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((900, 900))
    pygame.display.set_caption("Steppefall")
    return screen

def drawAll(screen, level, player_x, player_y, bullets):
    wy = 160
    pygame.draw.rect(screen, (0, 0, 255), (player_x, player_y, 40, 40))
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "B":
                pygame.draw.rect(screen, (0,255,0), (x*40, y*40+wy, 40, 40))
            elif level[y][x] == "L":
                pygame.draw.rect(screen, (255,0,0), (x*40, y*40+wy, 40, 40))
    for i in range(len(bullets)):
        if bullets[i] is not None:
            pygame.draw.rect(screen, (255, 255, 255), (bullets[i].x, bullets[i].y+wy, bullets[i].size_width, bullets[i].size_width))
    return screen


random.seed() 

def run(level):
    aBoard = board(level)
    aBoard.find_chest_contents()
    screen = start()
    player_1 = Pirate(level)
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_1.move(True, False)
        if keys[pygame.K_RIGHT]:
            player_1.move(False, True)
        
        if keys[pygame.K_SPACE]:
                player_1.jump()
        
        player_1.update_vy()
        screen = drawAll(screen, level, player_x=player_1.x, player_y=player_1.y, bullets=[player_1.current_attack, player_1.current_super])
        pygame.display.flip()
        clock.tick(40)
            

run(level)
a = board([])
a.find_chest_contents()
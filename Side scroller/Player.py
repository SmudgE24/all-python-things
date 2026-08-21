#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 18:29:29 2026

@author: ethanbrown
"""
import Items

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
        self.max_hp = hp

        self.inventory = {'armour':[], 
                          'item':[],
                          'weapon':[]}
        
        # Inventory management
        self.inventory_section = 'weapon'
        self.inventory_index = {'weapon': 0, 'armour': 0, 'item': 0}
        self.equipped = {'weapon': None, 'armour': None, 'item': None}
        self.base_speed = 5
        self.speed = self.base_speed
        self.damage = 1  # Base damage
        self.void_immune = False  # Immunity to void damage
        self.active_effects = Items.ItemEffect()  # Track active item effects
    
    def collect_coins(self):
        if self.is_on_wall("C", True):
            left = (self.x + 1) // 40
            right = (self.x + 39) // 40
            bottom = (self.y + 41) // 40
    
            if self.level[bottom][left] == "C":
                self.level[bottom][left] = "."
    
            if self.level[bottom][right] == "C":
                self.level[bottom][right] = "."
            self.coins += 1
            return True
        return False

    def move(self, left, right):
        Or = True
        block = "B"
        INVENTORY_WIDTH = 150  # Prevent player from entering inventory area
        MIN_X = INVENTORY_WIDTH / 40  # Convert to block units (40 pixels per block)
        
        if left:
            if not self.is_touching_wall_left(block, Or):
                for i in range(self.speed):
                    if not self.is_touching_wall_left(block, Or) and self.x > MIN_X:
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

        if self.vy > 12:
            self.vy = 12

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
        """Add item to appropriate inventory section"""
        if isinstance(item, str):
            if "Armour" in item or "Shield" in item:
                self.inventory['armour'].append(item)
            elif "Sword" in item or "Bow" in item or "Dagger" in item or "Cannon" in item:
                self.inventory['weapon'].append(item)
            else:
                self.inventory['item'].append(item)
    
    def switch_inventory_section(self):
        """Switch to next inventory section"""
        sections = ['weapon', 'armour', 'item']
        current_idx = sections.index(self.inventory_section)
        self.inventory_section = sections[(current_idx + 1) % len(sections)]
        self.inventory_index[self.inventory_section] = 0
    
    def scroll_inventory(self, direction):
        """Scroll through current inventory section"""
        section = self.inventory_section
        current_items = self.inventory[section]
        if not current_items:
            return
        self.inventory_index[section] += direction
        self.inventory_index[section] %= len(current_items)
    
    def equip_item(self):
        """Equip the currently selected item"""
        section = self.inventory_section
        items = self.inventory[section]
        if not items:
            return
        selected_item = items[self.inventory_index[section]]
        self.equipped[section] = selected_item
        self._apply_item_effects(selected_item)
    
    def _apply_item_effects(self, item_name=None):
        """Apply effects of equipped items"""
        self.speed = self.base_speed
        
        # Apply weapon effects
        if self.equipped.get('weapon'):
            try:
                weapon = Items.Item(self.equipped['weapon'])
                if "Bow" in self.equipped['weapon']:
                    self.speed += 1
            except ValueError:
                pass
        
        # Apply armour effects
        if self.equipped.get('armour'):
            try:
                armour = Items.Item(self.equipped['armour'])
            except ValueError:
                pass
        
        # Apply item effects
        if self.equipped.get('item') and item_name == self.equipped.get('item'):
            try:
                item = Items.Item(self.equipped['item'])
                item.apply_effect(self)
            except ValueError:
                pass

    def Take_item(self, item):
        for section in self.inventory:
            if item in self.inventory[section]:
                self.inventory[section].remove(item)
                return True
        return False
    
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
        self.hp = 3
        self.speed = 7
        self.damage = 4
        self.jumpmax = 2
        player.__init__(self, level, self.jumpmax, self.hp)
        
        # Start with a basic sword using item system
        self.inventory['weapon'].append("Sword +1")
        self.equipped['weapon'] = "Sword +1"
        self.base_speed = 7
        self.speed = 7
        self.max_hp = 3
    
    def attack(self):
        self.current_attack = weapon((0,0), player_x=(self.x+40), player_y=(self.y+40), size_width=40, size_hight=7, level=self.level)
    
    #def use_ability(self):
    
    def super_attack(self):
        if self.super_charged:
            self.super_charged = False
            if self.going_left:
                self.current_super = weapon((-10,0), player_x=(self.x+40), player_y=(self.y+40), size_width=40, size_hight=7, level=self.level)
            else:
                self.current_super = weapon((10,0), player_x=(self.x+40), player_y=(self.y+40), size_width=40, size_hight=7, level=self.level)
    
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
    
    def is_touching_enemy(self, enemy_x, enemy_y):
        """Check if weapon is touching an enemy"""
        if ((self.x < (enemy_x + 40) and (self.x + self.size_width) > enemy_x) and 
            (self.y < (enemy_y + 40) and (self.y + self.size_hight) > enemy_y)):
            return True
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
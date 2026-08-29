#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 13:43:45 2026

@author: ethanbrown
"""

class armour:
    def __init__(self, El_type, strength_number):
        
        self.El_type = El_type
        self.strength_number = strength_number
        if self.strength_number > 8:
            self.strength_number = 8
        self.resistances = {
            'FIRE': 1.0,
            'WATER': 1.25,   # Weak
            'EARTH': 0.75,   # Resistant
            'AIR': 1.0
        }
        
    def damage_after_armour(self, damage, damage_type=None):
        # Elemental modifiers first
        if damage_type is not None:
            damage *= self.resistances.get(damage_type, 1.0)
    
        damage = round(damage)
    
        # Block damage based on armour
        blocked = (self.strength_number - 1) // 2
        damage -= blocked
    
        return max(1, damage) - 1

a = armour("FIRE", 6)
print(a.damage_after_armour(5, "FIRE"))
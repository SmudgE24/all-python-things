#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Item System for Steppefall
Define item properties, effects, and special abilities here
"""

# Item Database: Define all items with their properties
ITEMS_DB = {
    # Weapons
    "Sword +1": {
        "type": "weapon",
        "damage": 1,
        "attack_speed": 1.0,
        "rarity": "common",
        "description": "Stab",
        "effect": "Stab"
    },
    "Sword +3": {
        "type": "weapon",
        "damage": 3,
        "attack_speed": 0.9,
        "rarity": "rare",
        "description": "Stab",
        "effect": "Stab"
    },
    "Dagger +1": {
        "type": "weapon",
        "damage": 1,
        "attack_speed": 1.5,
        "rarity": "common",
        "description": "Stab",
        "effect": "Stab"
    },
    "Bow": {
        "type": "weapon",
        "damage": 2,
        "attack_speed": 1.0,
        "rarity": "uncommon",
        "description": "Ranged weapon",
        "effect": "ranged"
    },
    "Flame Gun": {
        "type": "weapon",
        "damage": 2,
        "attack_speed": 0.8,
        "rarity": "rare",
        "description": "Burns enemies",
        "effect": "fire"
    },
    
    # Armour
    "Shield +1": {
        "type": "armour",
        "defense": 1,
        "rarity": "uncommon",
        "description": "Reduces damage by 1"
    },
    "Armour +1": {
        "type": "armour",
        "defense": 1,
        "rarity": "uncommon",
        "description": "Light armour"
    },
    "Armour +2": {
        "type": "armour",
        "defense": 2,
        "rarity": "rare",
        "description": "Heavy armour"
    },
    "Void boots": {
        "type": "armour",
        "defense": 0,
        "rarity": "rare",
        "description": "One time teleportation 8 blocks forward",
        "effect": "speed_teleport"
    },
    
    # Items
    "10 Coins": {
        "type": "item",
        "value": 10,
        "rarity": "common",
        "description": "Currency"
    },
    "Jump boots": {
        "type": "item",
        "rarity": "uncommon",
        "description": "Extra jump height",
        "effect": "jump_boost"
    },
    "+1 life": {
        "type": "item",
        "value": 1,
        "rarity": "rare",
        "description": "Restore 1 HP",
        "effect": "heal"
    },
    "Bottle o' healin": {
        "type": "item",
        "value": 3,
        "rarity": "uncommon",
        "description": "Restore 3 HP",
        "effect": "heal"
    },
    "Bomb": {
        "type": "item",
        "damage": 5,
        "rarity": "uncommon",
        "description": "Explodes on impact",
        "effect": "explosive"
    },
    "Key": {
        "type": "item",
        "rarity": "rare",
        "description": "Unlocks secret areas",
        "effect": "unlock"
    },
    "Time Freeze 15s": {
        "type": "item",
        "duration": 15,
        "rarity": "rare",
        "description": "Freezes time",
        "effect": "time_freeze"
    },
    "Orb of power +5": {
        "type": "item",
        "rarity": "rare",
        "description": "Increases damage",
        "effect": "power_boost",
        "value": 5
    }
}

class Item:
    """Represents an item instance"""
    def __init__(self, name):
        if name not in ITEMS_DB:
            raise ValueError(f"Item '{name}' not found in database")
        
        self.name = name
        self.properties = ITEMS_DB[name].copy()
        self.is_equipped = False
    
    def get_type(self):
        return self.properties.get("type")
    
    def get_damage(self):
        return self.properties.get("damage", 0)
    
    def get_defense(self):
        return self.properties.get("defense", 0)
    
    def get_effect(self):
        return self.properties.get("effect", None)
    
    def get_rarity(self):
        return self.properties.get("rarity", "common")
    
    def apply_effect(self, player, enemies=None):
        """Apply item effects to player"""
        effect = self.get_effect()
        
        if effect == "heal":
            amount = self.properties.get("value", 1)
            old_hp = player.hp
            player.hp = min(
                player.max_hp,
                player.hp + amount
            )
            restored = player.hp - old_hp
            print(f"{self.name} restored {restored} HP!")
            return True
        
        elif effect == "jump_boost":
            player.jumpmax += 1
            print(f"{self.name} increased jump height!")
            return True
        
        elif effect == "power_boost":
            boost = self.properties.get("value", 5)
            player.damage += boost
            print(f"{self.name} increased damage by {boost}!")
            return True
        
        elif effect == "speed_teleport":
            print(f"{self.name} grants void teleportation!")

            if player.going_left:
                for i in range(80):
                    player.move(True, False)
            else:
                for i in range(80):
                    player.move(False, True)
            
            return True
        
        elif effect == "time_freeze":
            duration = self.properties.get("duration", 15)
            print(f"{self.name} freezes time for {duration}s!")
            player.timefrozen = True
            return True
        
        elif effect == "explosive":
            print(f"{self.name} is ready to explode!")
            if enemies is not None:
                player.trigger_explosion(enemies)
                return True
            return False
        
        return False


class ItemEffect:
    """Handles persistent item effects on the player"""
    def __init__(self):
        self.active_effects = {}
    
    def add_effect(self, effect_name, duration=None):
        """Add an active effect"""
        self.active_effects[effect_name] = {
            "duration": duration,
            "elapsed": 0
        }
    
    def update_effects(self, delta_time=1):
        """Update effect durations"""
        expired = []
        for effect_name, data in self.active_effects.items():
            if data["duration"] is not None:
                data["elapsed"] += delta_time
                if data["elapsed"] >= data["duration"]:
                    expired.append(effect_name)
        
        for effect in expired:
            del self.active_effects[effect]
    
    def has_effect(self, effect_name):
        """Check if player has an active effect"""
        return effect_name in self.active_effects

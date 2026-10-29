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
    "Flame Thrower": {
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
        "description": "Currency",
        "effect": "coin_pack"
    },
    "Jump potion": {
        "type": "item",
        "rarity": "uncommon",
        "description": "Extra jump height",
        "effect": "jump_boost"
    },
    "+3 life": {
        "type": "item",
        "value": 3,
        "rarity": "very rare",
        "description": "Restore 3 HP",
        "effect": "heal"
    },
    "Healing potion": {
        "type": "item",
        "value": 1,
        "rarity": "uncommon",
        "description": "Restore 1 HP",
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
    
    },
    "Vitality Ring": {
        "type": "item",
        "rarity": "common",
        "description": "Increases maximum health",
        "effect": "health_max_boost",
        "value": 10
    },
    "Swiftness +1": {
        "type": "item",
        "rarity": "common",
        "description": "Increases movement speed",
        "effect": "speed_boost",
        "value": 1
    },
    "Iron Skin +5": {
        "type": "item",
        "rarity": "common",
        "description": "Reduces damage taken",
        "effect": "damage_resistance",
        "value": 5
    },
    "Lucky Coin": {
        "type": "item",
        "rarity": "common",
        "description": "Increases coins found",
        "effect": "coin_boost",
        "value": 10
    },
    "Small Charm": {
        "type": "item",
        "rarity": "common",
        "description": "Restores health when defeating an enemy",
        "effect": "health_on_kill",
        "value": 2
    },
    "Wind Feather": {
        "type": "item",
        "rarity": "uncommon",
        "description": "Increases jump height",
        "effect": "jump_boost",
        "value": 2
    },
    "Protection Ring": {
        "type": "item",
        "rarity": "uncommon",
        "description": "Reduces damage taken",
        "effect": "damage_resistance",
        "value": 10
    },
    "Moon Tear": {
        "type": "item",
        "rarity": "uncommon",
        "description": "Increases the chance of finding rare loot",
        "effect": "luck_boost",
        "value": 10
    },
    # "Gauntlet of the Earth": {
    #     "type": "item",
    #     "rarity": "uncommon",
    #     "description": "Increases damage dealt to breakable blocks",
    #     "effect": "block_damage",
    #     "value": 25
    # },
    "Bloodstone": {
        "type": "item",
        "rarity": "uncommon",
        "description": "Restores health when defeating an enemy",
        "effect": "health_on_kill",
        "value": 5
    },
    "Ember Heart": {
        "type": "item",
        "rarity": "rare",
        "description": "Reduces damage taken from lava",
        "effect": "lava_resistance",
        "value": 50
    },
    "Fury Crystal": {
        "type": "item",
        "rarity": "rare",
        "description": "Increases damage dealt by 30 percent",
        "effect": "power_percent_boost",
        "value": 30
    },
    # "Shadow Cloak": {
    #     "type": "item",
    #     "rarity": "rare",
    #     "description": "Reduces the distance at which enemies detect you",
    #     "effect": "stealth_boost",
    #     "value": 50
    # },
    # "Storm Core": {
    #     "type": "item",
    #     "rarity": "rare",
    #     "description": "Increases attack speed",
    #     "effect": "attack_speed",
    #     "value": 25
    # },
    # "Khan's Eye": {
    #     "type": "item",
    #     "rarity": "rare",
    #     "description": "Reveals nearby hidden rooms",
    #     "effect": "secret_detection",
    #     "value": 1
    # },
    "Broken Crown": {
        "type": "item",
        "rarity": "very rare",
        "description": "Increases damage by 50 percent but reduces maximum health by 20 percent",
        "effect": "cursed_power",
        "value": 50
    },
    "Phoenix Feather": {
        "type": "item",
        "rarity": "very rare",
        "description": "Revives you once after a fatal hit",
        "effect": "second_chance",
        "value": 1
    },
    # "Hourglass of Time": {
    #     "type": "item",
    #     "rarity": "very rare",
    #     "description": "Slows nearby enemies temporarily",
    #     "effect": "enemy_slow",
    #     "value": 50
    # },
    "Greed's Emblem": {
        "type": "item",
        "rarity": "very rare",
        "description": "Doubles coins found from enemies and chests",
        "effect": "coin_multiplier",
        "value": 2
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
            player.hp += amount
            if player.hp > player.max_hp:
                player.hp = player.max_hp
            restored = player.hp - old_hp
            print(f"{self.name} restored {restored} HP!")
            return restored > 0

        elif effect == "coin_pack":
            amount = self.properties.get("value", 0)
            coins_gained = player.gain_coins(amount)
            print(f"{self.name} added {coins_gained} coins!")
            return True

        elif effect == "unlock":
            player.secret_room_unlocked = True
            print(f"{self.name} unlocked a secret area!")
            return True
        
        elif effect == "jump_boost":
            boost = self.properties.get("value", 1)
            player.jumpmax += boost
            print(f"{self.name} increased jump height by {boost}!")
            return True
        
        elif effect == "power_boost":
            boost = self.properties.get("value", 5)
            player.damage += boost
            print(f"{self.name} increased damage by {boost}!")
            return True
        
        elif effect == "speed_teleport":
            print(f"{self.name} grants void teleportation!")
            direction = -1 if player.going_left else 1
            for _ in range(8 * 40):
                if direction < 0:
                    if player.is_touching_wall_left("B", True):
                        break
                elif player.is_touching_wall_right("B", True):
                    break
                player.x += direction
            
            return True
        
        elif effect == "time_freeze":
            duration = self.properties.get("duration", 15)
            print(f"{self.name} freezes time for {duration}s!")
            player.timefrozen = True
            player.timefrozen_duration = duration
            return True

        elif effect == "explosive":
            print(f"{self.name} is ready to explode!")
            if enemies is not None:
                player.trigger_explosion(
                    enemies,
                    self.properties.get("damage", 5)
                )
                return True
            return False

        elif effect == "health_max_boost":
            boost = self.properties.get("value", 10)
            player.max_hp += boost
            player.hp += boost
            print(f"{self.name} increased maximum health by {boost}!")
            return True

        elif effect == "speed_boost":
            boost = self.properties.get("value", 1)
            player.speed_bonus += boost
            player.speed += boost
            print(f"{self.name} increased movement speed by {boost}!")
            return True

        elif effect == "damage_resistance":
            boost = self.properties.get("value", 5)
            player.resistance += boost
            print(f"{self.name} increased damage resistance by {boost}!")
            return True

        elif effect == "coin_boost":
            boost = self.properties.get("value", 10)
            player.coin_chance = min(100, player.coin_chance + boost)
            print(f"{self.name} increased coin drop chance by {boost}%!")
            return True

        elif effect == "coin_multiplier":
            player.coin_multiplier *= self.properties.get("value", 2)
            print(f"{self.name} multiplies coins found!")
            return True

        elif effect == "health_on_kill":
            boost = self.properties.get("value", 2)
            player.health_on_kill += boost
            print(f"{self.name} will restore {boost} HP on enemy kills!")
            return True

        elif effect == "lava_resistance":
            boost = self.properties.get("value", 50)
            player.lava_resistance += boost
            print(f"{self.name} increased lava resistance by {boost}!")
            return True

        elif effect == "cursed_power":
            boost = self.properties.get("value", 50)
            player.damage_multiplier *= 1 + boost / 100
            player.max_hp = int(player.max_hp * 0.8)
            if player.max_hp < 1:
                player.max_hp = 1
            if player.hp > player.max_hp:
                player.hp = player.max_hp
            print(f"{self.name} increased damage by {boost}% but reduced max HP by 20%!")
            return True

        elif effect == "second_chance":
            player.revive += 1
            print(f"{self.name} grants a second chance upon death!")
            return True

        elif effect == "luck_boost":
            player.luck += self.properties.get("value", 1)
            print(f"{self.name} improved rare loot chances!")
            return True

        elif effect == "power_percent_boost":
            boost = self.properties.get("value", 30)
            player.damage_multiplier *= 1 + boost / 100
            print(f"{self.name} increased damage by {boost}%!")
            return True
        
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

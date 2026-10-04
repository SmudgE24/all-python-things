import Player

class boss:
    def __init__(self, level, jumpmax, hp, type):
        self.level = level
        self.jumpmax = jumpmax
        self.hp = hp
        self.type = type
        if self.type == "fire":
            
        Player.player.__init__(self, level, self.jumpmax, self.hp)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"{self.name} has been defeated!")
        else:
            print(f"{self.name} has {self.health} health remaining.")

    def attack(self):
        return self.attack_power
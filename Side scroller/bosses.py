import Player

class fire_boss:
    def __init__(self, level, jumpmax, hp):
        self.level = level
        self.jumpmax = jumpmax
        self.hp = hp
        self.name = "Fire Boss"
        Player.player.__init__(self, level, self.jumpmax, self.hp)
        attackCurrents = []

    def attack(self):
        self.attackCurrents.append(Player.weapon((10, 0), self.x, self.y, 10, 10, self.level, "ranged"))

    def updateAttack(self):
        toRemove = []
        a = False
        for i in range(len(self.attackCurrents)):
            a = self.attackCurrents[i].move()
            if a:
                toRemove.append(self.attackCurrents[i])
        for attack in toRemove:
            self.attackCurrents.remove(attack)

    def run(self, player_x, player_y):
        self.updateAttack()
        if player_x > self.x:
            self.move()
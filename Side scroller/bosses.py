import Player


class fire_boss(Player.player):
    def __init__(self, level):
        self.jumpmax = 5
        self.hp = 3670
        self.name = "Fire Boss"
        super().__init__(level, self.jumpmax, self.hp)
        self.hight = 80
        self.speed = 3
        self.max_hp = self.hp
        self.attackCurrents = []
        self.attack_timer = 0
        self.contact_cooldown = 0

    def attack(self, player_x):
        direction = -10 if player_x < self.x else 10
        attack_x = self.x - 280 if direction < 0 else self.x + self.width
        self.attackCurrents.append(
            Player.weapon(
                (direction, 0), attack_x, self.y + self.hight // 2,
                10, 10, self.level, "ranged"
            )
        )

    def updateAttack(self):
        for attack in self.attackCurrents[:]:
            if (
                attack.move()
                or attack.x + attack.size_width < 0
                or attack.x > len(self.level[0]) * 40
            ):
                self.attackCurrents.remove(attack)

    def is_lava_at(self, x, y):
        return (
            0 <= y < len(self.level)
            and 0 <= x < len(self.level[y])
            and str(self.level[y][x]).startswith("L")
        )

    def run(self, player_x, player_y):
        self.updateAttack()
        if self.contact_cooldown > 0:
            self.contact_cooldown -= 1
        self.attack_timer += 1
        if self.attack_timer >= 80:
            self.attack(player_x)
            self.attack_timer = 0

        buffer = 7 * 40
        if player_x > self.x + buffer:
            left, right = False, True
        elif player_x < self.x - buffer:
            left, right = True, False
        elif player_x > self.x:
            left, right = True, False
        elif player_x < self.x:
            left, right = False, True
        else:
            left, right = False, False

        lava_y = (self.y + self.hight + 15) // 40
        if left and self.is_lava_at((self.x - 1) // 40, lava_y):
            left = False
        if right and self.is_lava_at((self.x + self.width) // 40, lava_y):
            right = False

        self.move(left, right)

        if (
            (left and self.is_touching_wall_left("B", True))
            or (right and self.is_touching_wall_right("B", True))
            or self.y > player_y + 20
        ):
            self.jump()

    def isTouchingPlayer(self, player):
        overlaps = (
            player.x < self.x + self.width
            and player.x + player.width > self.x
            and player.y < self.y + self.hight
            and player.y + player.hight > self.y
        )
        if not overlaps:
            return None
        if player.vy > 0 and player.last_y + player.hight <= self.y + 5:
            return "stomp"
        return "hit"

    def is_touching_weapon(self, attack):
        if attack.attack_type == "fire":
            for fire_x, fire_y in attack.positions or []:
                if (
                    fire_x * 40 < self.x + self.width
                    and fire_x * 40 + 40 > self.x
                    and fire_y * 40 < self.y + self.hight
                    and fire_y * 40 + 40 > self.y
                ):
                    attack.expired = True
                    return True
            return False

        overlaps = (
            attack.x < self.x + self.width
            and attack.x + attack.size_width > self.x
            and attack.y < self.y + self.hight
            and attack.y + attack.size_hight > self.y
        )
        if overlaps:
            attack.expired = True
        return overlaps

    def is_attack_touching_player(self, attack, player):
        overlaps = (
            attack.x < player.x + player.width
            and attack.x + attack.size_width > player.x
            and attack.y < player.y + player.hight
            and attack.y + attack.size_hight > player.y
        )
        if overlaps:
            attack.expired = True
        return overlaps

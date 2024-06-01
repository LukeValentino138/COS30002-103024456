from weapon import Weapon
from projectile import Projectile

class Rifle(Weapon):
    def fire(self, target_pos):
        return Projectile(self.owner.pos, target_pos, speed=500, accuracy=0.99)

class Rocket(Weapon):
    def fire(self, target_pos):
        return Projectile(self.owner.pos, target_pos, speed=200, accuracy=0.80)

class Pistol(Weapon):
    def fire(self, target_pos):
        return Projectile(self.owner.pos, target_pos, speed=450, accuracy=0.35)

class Grenade(Weapon):
    def fire(self, target_pos):
        return Projectile(self.owner.pos, target_pos, speed=130, accuracy=0.2)

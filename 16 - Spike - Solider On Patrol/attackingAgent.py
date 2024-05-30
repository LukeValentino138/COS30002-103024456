from vector2d import Vector2D
from agent import Agent
from graphics import egi, KEY
from weapons import Rifle, Rocket, Pistol, Grenade
from path import Path

class AttackingAgent(Agent):

    def __init__(self, world=None, scale=30.0, mass=1.0):
        super(AttackingAgent, self).__init__(world, scale, mass, mode='follow_path')
        self.color = 'RED'
        self.pos = Vector2D(100,250)
        self.current_weapon = Rifle(self)
        self.projectiles = []
        self.path = Path()
        self.randomise_path()

    WEAPON_MODES = {
        KEY.F1: 'rifle',
        KEY.F2: 'rocket',
        KEY.F3: 'pistol',
        KEY.F4: 'grenade',
    }

    def select_weapon(self, weapon_mode):
        if weapon_mode == 'rifle':
            self.current_weapon = Rifle(self)
        elif weapon_mode == 'rocket':
            self.current_weapon = Rocket(self)
        elif weapon_mode == 'pistol':
            self.current_weapon = Pistol(self)
        elif weapon_mode == 'grenade':
            self.current_weapon = Grenade(self)

    def fire_weapon(self, target_pos):
        projectile = self.current_weapon.fire(target_pos)
        self.projectiles.append(projectile)

    def calculate(self, delta):
        mode = self.mode
        if mode == 'follow_path':
            force = self.follow_path()
        else:
            force = super(AttackingAgent, self).calculate(delta)
        self.force = force
        return force

    def update(self, delta):
        # use inherited update + addon
        super().update(delta)
        for projectile in self.projectiles:
            projectile.update(delta)

    def render(self):
        # use inherited render + addon
        super().render()
        for projectile in self.projectiles:
            projectile.render()

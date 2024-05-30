from agent import Agent
from graphics import KEY
from vector2d import Vector2D

class AttackingAgent(Agent):
    def __init__(self, world=None, scale=30.0, mass=1.0):
        super(AttackingAgent, self).__init__(world, scale, mass, mode='stationary')
        self.color = 'RED'
        self.pos = Vector2D(100,250)

    WEAPON_MODES = {
    KEY.F1: 'rifle',
    KEY.F2: 'rocket',
    KEY.F3: 'pistol',
    KEY.F4: 'grenade',
    }

    def calculate(self, delta):
        mode = self.mode
        if mode == 'stationary':
            force = Vector2D()
        else:
            force = super(AttackingAgent, self).calculate(delta)
        self.force = force
        return force

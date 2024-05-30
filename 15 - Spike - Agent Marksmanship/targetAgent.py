from agent import Agent
from path import Path
from vector2d import Vector2D

class TargetAgent(Agent):
    def __init__(self, world=None, scale=30.0, mass=1.0):
        super(TargetAgent, self).__init__(world, scale, mass, mode='follow_path')
        self.color = 'BLUE'
        self.path = Path(looped=True)
        waypoints = [Vector2D(400, 100), Vector2D(400, 400)]
        self.set_path(waypoints)

    def set_path(self, waypoints):
        self.path.set_pts(waypoints)

    def calculate(self, delta):
        mode = self.mode
        if mode == 'follow_path':
            force = self.follow_path()
        else:
            force = super(TargetAgent, self).calculate(delta)
        self.force = force
        return force

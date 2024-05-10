from graphics import egi, KEY
from math import cos, sin, pi
from point2d import Point2D

class Agent(object):
    def __init__(self, start, target):
        self.path = None
        self.start = start
        self.target = target
        self.pos = start._vc
        self.radius = 10

    def update(self, dt):
        if self.target is not None:
            # Calculate the direction vector from current position to the target
            direction = self.target._vc - self.start._vc
            # Normalize the direction vector
            direction.normalize()

            # Agent speed
            speed = 25 

            # Update the position based on speed and direction
            self.pos += direction * speed * dt

    def render(self):
        egi.blue_pen()
        egi.circle(pos=self.pos, radius=self.radius, filled=True)

    def draw_target(self):
        if self.target is not None:
            egi.red_pen()
            egi.circle(pos=self.target, radius=5, filled=True)


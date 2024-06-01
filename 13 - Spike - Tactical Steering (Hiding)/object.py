from graphics import egi, KEY

from vector2d import Vector2D


class Object(object):
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius
    
    def render(self):
        # Code to draw the object as a circle
        egi.circle(self.position, self.radius)

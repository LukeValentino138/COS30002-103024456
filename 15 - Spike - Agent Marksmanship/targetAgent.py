from agent import Agent
from path import Path
from vector2d import Vector2D
from point2d import Point2D
from math import pi, sin, cos
from graphics import egi, KEY

class TargetAgent(Agent):
    def __init__(self, world=None, scale=30.0, mass=1.0):
        super(TargetAgent, self).__init__(world, scale, mass, mode='follow_path')
        self.color = 'BLUE'
        self.path = Path(looped=True)
        waypoints = [Vector2D(400, 50), Vector2D(400, 450)]
        self.set_path(waypoints)
        self.pos = Vector2D(400, 50)

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

    def render(self, color=None):
        ''' Draw the triangle agent with color'''
        # draw the path if it exists and the mode is follow
        if self.mode == 'follow_path':
            self.path.render()
            pass

        # draw the ship
        egi.set_pen_color(name=self.color)
        pts = self.world.transform_points(self.vehicle_shape, self.pos,
                                          self.heading, self.side, self.scale)
        # draw it!
        egi.circle(self.pos, self.bRadius)

        # add some handy debug drawing info lines - force and velocity
        if self.show_info:
            s = 0.5 # <-- scaling factor
            # force
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
            # velocity
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
            # net (desired) change
            egi.white_pen()
            egi.line_with_arrow(self.pos+self.vel * s, self.pos+ (self.force+self.vel) * s, 5)
            egi.line_with_arrow(self.pos, self.pos+ (self.force+self.vel) * s, 5)
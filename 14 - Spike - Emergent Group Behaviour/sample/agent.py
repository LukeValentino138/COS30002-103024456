'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without permission.

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange, uniform
from path import Path

AGENT_MODES = {
    KEY._1: 'wander',
    KEY._2: 'separation',
    KEY._3: 'alignment',
    KEY._4: 'combined'
}

class Agent(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.9,
        'normal': 0.5,
        'fast': 0.1
        ### ADD 'normal' and 'fast' speeds here
    }

    def __init__(self, world=None, scale=30.0, mass=1.0, mode='wander'):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random start pos
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()  # current steering force
        self.accel = Vector2D()  # current acceleration due to force
        self.mass = mass

        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]
        self.waypoint_threshold = 40.0

        # NEW WANDER INFO
        self.wander_target = Vector2D(1, 0)
        self.wander_dist = 1.0 * scale
        self.wander_radius = 1.0 * scale
        self.wander_jitter = 10.0 * scale
        self.bRadius = scale
        self.max_speed = 5.0 * scale
        self.max_force = 500.0

        # SPIKE 14 NEIGHBOURS
        self.neighbours = []
        self.neighbour_radius = 100.0

        # Parameters for steering behaviors
        self.wander_amount = 1.0
        self.separation_amount = 75.0

        # debug draw info?
        self.show_info = False

    def calculate(self, delta):
        # Initialize the steering force
        SteeringForce = Vector2D()

        if self.mode == 'wander':
            # Apply Wander behavior
            SteeringForce += self.wander(delta) * self.wander_amount

        elif self.mode == 'separation':
            # Apply Separation behavior
            SteeringForce += self.separation(self.neighbours) * self.separation_amount
        
        elif self.mode == 'alignment':
            # Apply Alignment behavior
            SteeringForce += self.alignment(self.neighbours)

        elif self.mode == 'combined':
            # Apply both behaviors with weighted sum
            SteeringForce += self.wander(delta) * self.wander_amount
            SteeringForce += self.separation(self.neighbours) * self.separation_amount
            SteeringForce += self.alignment(self.neighbours)

        # Truncate the steering force to the maximum allowed
        SteeringForce.truncate(self.max_force)

        return SteeringForce

    def update(self, delta):
        ''' update vehicle position and orientation '''
        # calculate and set self.force to be applied
        ## force = self.calculate()
        force = self.calculate(delta)  # <-- delta needed for wander
        force.truncate(self.max_force)
        ## limit force? <-- for wander
        # ...
        # determine the new acceleration
        self.accel = force / self.mass  # not needed if mass = 1.0
        # new velocity
        self.vel += self.accel * delta
        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.lengthSq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)

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
        egi.closed_shape(pts)

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

        if self.mode == 'wander' or self.mode == 'combined':
            # calculate the center of the wander circle in front of the agent
            wnd_pos = Vector2D(self.wander_dist, 0)
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            # draw the wander circle
            egi.green_pen()
            egi.circle(wld_pos, self.wander_radius)
            # draw the wander target (little circle on the big circle)
            egi.red_pen()
            wnd_pos = (self.wander_target + Vector2D(self.wander_dist, 0))
            wld_pos = self.world.transform_point(wnd_pos, self.pos, self.heading, self.side)
            egi.circle(wld_pos, 3)

    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def TagNeighbours(self, bots, radius):
        """ Tag neighbours within a given radius """
        self.neighbours = []
        for bot in bots:
            if bot != self:
                to = self.pos - bot.pos
                gap = radius + bot.bRadius
                if to.lengthSq() < gap**2:
                    self.neighbours.append(bot)
    
    def separation(self, group):
        SteeringForce = Vector2D()
        for bot in group:
            # Don’t include self, only include neighbors (already tagged)
            if bot != self and bot in self.neighbours:
                ToBot = self.pos - bot.pos
                # Scale based on inverse distance to neighbor
                if ToBot.lengthSq() > 0:  # Avoid division by zero
                    SteeringForce += ToBot.normalise() / ToBot.length()
        return SteeringForce
    
    def alignment(self, group):
        AverageHeading = Vector2D()
        NeighborCount = 0

        for bot in group:
            # Don’t include self, only include neighbors
            if bot != self and bot in self.neighbours:
                AverageHeading += bot.heading
                NeighborCount += 1

        if NeighborCount > 0:
            AverageHeading /= NeighborCount
            AverageHeading = AverageHeading.normalise() * self.max_speed
            AverageHeading -= self.vel

        return AverageHeading


    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)
        
    def wander(self, delta):
        ''' random wandering using a projected jitter circle '''
        wt = self.wander_target
        # this behaviour is dependent on the update rate, so this line must
        # be included when using time independent framerate.
        jitter_tts = self.wander_jitter * delta # this time slice
        # first, add a small random vector to the target's position
        wt += Vector2D(uniform(-1,1) * jitter_tts, uniform(-1,1) * jitter_tts)
        # re-project this new vector back on to a unit circle
        wt.normalise()
        # increase the length of the vector to the same as the radius
        # of the wander circle
        wt *= self.wander_radius
        # move the target into a position WanderDist in front of the agent
        target = wt + Vector2D(self.wander_dist, 0)
        # project the target into world space
        wld_target = self.world.transform_point(target, self.pos, self.heading, self.side)
        # and steer towards it
        return self.seek(wld_target)



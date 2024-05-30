from agent import Agent
from path import Path
from vector2d import Vector2D
from graphics import egi

class TargetAgent(Agent):
    def __init__(self, world=None, scale=30.0, mass=1.0):
        super(TargetAgent, self).__init__(world, scale, mass, mode='patrol')
        self.color = 'BLUE'
        self.hit_color = 'RED'  
        self.current_color = self.color  
        self.path = Path(looped=True)
        waypoints = [Vector2D(400, 50), Vector2D(400, 450)]
        self.set_path(waypoints)
        self.pos = Vector2D(400, 250)
        self.radius = scale  # radius of the target for collision detection
        self.hit_duration = 0.5  #
        self.hit_timer = 0

    def set_path(self, waypoints):
        self.path.set_pts(waypoints)

    def calculate(self, delta):
        mode = self.mode
        if mode == 'patrol':
            force = self.follow_path()
        else:
            force = super(TargetAgent, self).calculate(delta)
        self.force = force
        return force

    def update(self, delta):
        super().update(delta)
        self.check_collision()
        if self.hit_timer > 0:
            self.hit_timer -= delta
            if self.hit_timer <= 0:
                self.hit_timer = 0  # stops the timer from being negative

    def check_collision(self):
        for projectile in self.world.attackingAgent.projectiles:
            if (self.pos - projectile.pos).length() < self.radius:
                self.handle_hit(projectile)

    def handle_hit(self, projectile):
        # remove the projectile
        self.world.attackingAgent.projectiles.remove(projectile)
        print("Hit detected!")
        # set hit timer
        self.hit_timer = self.hit_duration


    def render(self, color=None):
        # draw the path if it exists and the mode is follow
        if self.mode == 'follow_path':
            self.path.render()
            pass


        current_color = self.hit_color if self.hit_timer > 0 else self.color

        egi.set_pen_color(name=current_color)
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
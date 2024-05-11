from graphics import egi, KEY
from math import cos, sin, pi
from point2d import Point2D

from math import sqrt

class Agent(object):
    def __init__(self, start, target, world, speed, radius, waypoint_near_dist=3):
        # Initializes the agent with start and target positions, world context, speed, radius, and proximity threshold for waypoints
        self.start = start
        self.target = target
        self.world = world
        self.path = None
        self.current_node_index = 0
        self.pos = start._vc
        self.radius = radius
        self.speed = speed
        self.waypoint_near_dist = waypoint_near_dist
        self.at_final_target = False

    def update(self, dt):
        # Updates the agent's state every frame; checks path status and moves towards the current target or handles arrival
        if self.path and not self.path_finished() and not self.at_final_target:
            if self.is_near_waypoint():
                self.next_waypoint()
            if not self.path_finished():
                self.seek(self.current_target(), dt)
            else:
                self.arrive(self.path.end_point(), dt)
        elif self.path_finished() or self.at_final_target:
            self.at_final_target = True

    def is_near_waypoint(self):
        # Checks if the agent is near the current waypoint based on the defined near distance threshold
        current_target = self.current_target()
        distance = sqrt((current_target.x - self.pos.x)**2 + (current_target.y - self.pos.y)**2)
        return distance < self.waypoint_near_dist

    def current_target(self):
        # Returns the current waypoint
        return self.world.boxes[self.path.path[self.current_node_index]]._vc

    def next_waypoint(self):
        # Advances the waypoint index to the next one in the path unless it's the last one
        if self.current_node_index < len(self.path.path) - 1:
            self.current_node_index += 1
        else:
            self.at_final_target = True

    def path_finished(self):
        # Checks if the agent has reached the end of the path.
        return self.current_node_index >= len(self.path.path)

    def seek(self, target_pos, dt):
        # Moves the agent towards the target position following a direct path
        direction = target_pos - self.pos
        direction.normalize()
        self.pos += direction * self.speed * dt

    def arrive(self, target_pos, dt):
        # Moves the agent towards the target position. If target is in proximity threshold, 
        # sets the position to the target and stops movement
        direction = target_pos - self.pos
        distance = sqrt(direction.x**2 + direction.y**2)
        if distance <= self.waypoint_near_dist:
            self.pos = target_pos
            self.at_final_target = True

    def render(self):
        # Renders the agent as a circle with a specified color and radius
        egi.set_pen_color(self.color)
        egi.circle(pos=self.pos, radius=self.radius, filled=True)

    def draw_target(self):
        # Draws the agent's target as a circle if it exists
        if self.target is not None:
            egi.red_pen()
            egi.circle(pos=self.target._vc, radius=5, filled=True)


class FastAgent(Agent):
    def __init__(self, start, target, world):
        Agent.__init__(self, start, target, world, speed=100, radius=10)
        self.color = (0, 1, 0, 1) 

class SlowAgent(Agent):
    def __init__(self, start, target, world):
        Agent.__init__(self, start, target, world, speed=25, radius=15)
        self.color = (1, 0, 0, 1) 
from vector2d import Vector2D
from agent import Agent
from graphics import egi, KEY
from weapons import Rifle, Rocket, Pistol, Grenade
from path import Path
from statemachine import StateMachine
from patrolState import PatrolState

class AttackingAgent(Agent):

    def __init__(self, world=None, scale=30.0, mass=1.0):
        super(AttackingAgent, self).__init__(world, scale, mass, mode='patrol')
        self.color = 'RED'
        self.pos = Vector2D(450, 250)
        self.current_weapon = Rifle(self)
        self.projectiles = []
        self.randomise_path()
        self.detection_radius = 100.0 
        self.max_speed = 5 * scale

        self.fsm = StateMachine(self)
        self.fsm.change_state(PatrolState())

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
        return self.force

    def update(self, delta):
        self.fsm.update(delta) 

        self.force.truncate(self.max_force)  

        self.accel = self.force / self.mass  

        self.vel += self.accel * delta  
        self.vel.truncate(self.max_speed)  

        self.pos += self.vel * delta

        if self.vel.lengthSq() > 0.00000001: 
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()

        self.world.wrap_around(self.pos)

        for projectile in self.projectiles:
            projectile.update(delta)

    def render(self):
        super().render()
        for projectile in self.projectiles:
            projectile.render()

    def seek_waypoint(self):
        current_waypoint = self.path.current_pt()
        return self.seek(current_waypoint)

    def check_waypoint_distance(self):
        current_waypoint = self.path.current_pt()
        if current_waypoint and self.pos.distanceSq(current_waypoint) < self.waypoint_threshold ** 2:
            return True
        return False

    def get_next_waypoint(self):
        self.path.inc_current_pt()

    def detect_enemy(self):
        for agent in self.world.agents:
            if agent is not self:  # Don't check against itself
                distance = self.pos.distance(agent.pos)
                if distance < self.detection_radius:
                    return agent  # Return the detected enemy
        return None
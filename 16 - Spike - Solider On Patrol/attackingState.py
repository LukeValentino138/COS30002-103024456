from state import State
from statemachine import StateMachine
from vector2d import Vector2D
import time

class ShootingState(State):
    def __init__(self, enemy):
        self.enemy = enemy

    def start(self, agent):
        print("Entering Shooting State")
        pass

    def running(self, agent, delta):
        print("Entering shooting running State")
        agent.fire_weapon(self.enemy)
        agent.attack_fsm.change_state(ReloadingState())


class ReloadingState(State):
    def start(self, agent):
        self.start_time = time.time()

    def running(self, agent, delta):
        current_time = time.time()
        if current_time - self.start_time >= 2.0:  # 2 second delay
            agent.attack_fsm.change_state(AttackingState())


class AttackingState(State):
    def start(self, agent):
        print("Entering Attack State")
        agent.attack_fsm = StateMachine(agent)
        agent.force = Vector2D()  # Stop the agent 
        agent.vel = Vector2D()
        self.enemy = agent.detect_enemy()
        if self.enemy:
            agent.attack_fsm.change_state(ShootingState(self.enemy))
        else:
            from patrolState import PatrolState
            agent.fsm.change_state(PatrolState())

    def running(self, agent, delta):
        agent.attack_fsm.update(delta)
        if not agent.detect_enemy():
            from patrolState import PatrolState
            agent.fsm.change_state(PatrolState())

        

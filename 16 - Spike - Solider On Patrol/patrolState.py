from state import State
from statemachine import StateMachine
from vector2d import Vector2D

class SeekState(State):
    def start(self, agent):
        print("Entering Seek State")

    def running(self, agent, delta):
        print("Running Seek State")
        agent.force = agent.seek_waypoint()

class ArriveState(State):
    def start(self, agent):
        print("Entering Arrive State")
        agent.path.inc_current_pt()  # Move to the next waypoint
        if agent.path.is_finished():
            return Vector2D()

    def running(self, agent, delta):
        # Directly move to the next waypoint after arriving
        agent.patrol_fsm.change_state(SeekState())

class PatrolState(State):
    def start(self, agent):
        print("Entering Patrol State")
        agent.patrol_fsm = StateMachine(agent)
        agent.patrol_fsm.change_state(SeekState())

    def running(self, agent, delta):
        print("Running Patrol State")
        agent.patrol_fsm.update(delta)
        if agent.check_waypoint_distance():
            print("Agent Reached Waypoint")
            agent.patrol_fsm.change_state(ArriveState())
        if agent.detect_enemy():
            print("Enemy Detected")
            from attackingState import AttackingState  # Deferred import
            agent.fsm.change_state(AttackingState())
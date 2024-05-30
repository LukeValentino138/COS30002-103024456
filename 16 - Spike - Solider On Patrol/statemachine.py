class StateMachine:
    def __init__(self, agent):
        self.agent = agent
        self.current_state = None

    def change_state(self, new_state):
        self.current_state = new_state
        if self.current_state:  # Ensure the new state is not None
            self.current_state.start(self.agent)

    def update(self, delta):
        if self.current_state:
            self.current_state.running(self.agent, delta)
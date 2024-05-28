from agent import Agent

class Hunter(Agent):
    def __init__(self, world=None, scale=30.0, mass=1.0):
        super(Hunter, self).__init__(world, scale, mass, mode='wander')
        self.color = 'RED'
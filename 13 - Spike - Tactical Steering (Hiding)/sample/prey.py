from agent import Agent

class Prey(Agent):
    def __init__(self, world=None, scale=30.0, mass=1.0):
        super(Prey, self).__init__(world, scale, mass, mode='flee')
        self.color = 'BLUE'

from agent import Agent

class Prey(Agent):
    def __init__(self, world=None, scale=30.0, mass=1.0):
        super(Prey, self).__init__(world, scale, mass, mode='hide')
        self.color = 'BLUE'

    def Hide(self, hunter, objs):
        DistToClosest = float('inf')
        BestHidingSpot = None
        # check for possible hiding spots
        for obj in objs:
            HidingSpot = self.world.GetHidingPosition(hunter.pos, obj.position, obj.radius)
            HidingDist = (HidingSpot - self.pos).lengthSq()
            if HidingDist < DistToClosest:
                DistToClosest = HidingDist
                BestHidingSpot = HidingSpot
        # if we have a best hiding spot, use it
        if BestHidingSpot:
            return self.arrive(BestHidingSpot, 'fast')
        # default - run away!
        return self.evade(hunter)
    
    def calculate(self, delta):
        mode = self.mode
        if mode == 'hide':
            force = self.Hide(self.world.hunter, self.world.objects)
        else:
            force = super(Prey, self).calculate(delta)
        self.force = force
        return force

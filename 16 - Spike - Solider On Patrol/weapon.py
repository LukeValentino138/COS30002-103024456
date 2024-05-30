class Weapon:
    def __init__(self, owner):
        self.owner = owner

    def fire(self, target_pos):
        raise NotImplementedError("This method should be overridden by subclasses")

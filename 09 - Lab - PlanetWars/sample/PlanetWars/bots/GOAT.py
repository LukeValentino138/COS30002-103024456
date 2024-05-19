from random import choice

class GOAT(object):

    def update(self, gameinfo):
        if gameinfo.my_planets and gameinfo.not_my_planets:
            src = max(gameinfo.my_planets.values(), key=lambda p: p.num_ships)
            # Find a target planet with the minimum number of ships.
            dest = min(gameinfo.not_my_planets.values(), key=lambda p: p.num_ships)
            if src.num_ships > 10:
                gameinfo.planet_order(src, dest, int(src.num_ships * 0.75) )
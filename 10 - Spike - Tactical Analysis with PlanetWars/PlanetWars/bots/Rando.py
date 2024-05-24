from random import choice

class Rando(object):

    def update(self, gameinfo):
        if gameinfo.my_planets and gameinfo.not_my_planets:
            # select random target and destination
            dest = choice(list(gameinfo.not_my_planets.values()))
            src = choice(list(gameinfo.my_planets.values()))
            # launch new fleet if there's enough ships
            if src.num_ships > 10:
                gameinfo.planet_order(src, dest, int(src.num_ships * 0.75) )
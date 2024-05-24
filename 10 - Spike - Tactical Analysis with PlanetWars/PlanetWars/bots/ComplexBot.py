class ComplexBot(object):

    def update(self, gameinfo):
        if gameinfo:
            print("All planets:")
            for planet in gameinfo.planets.values():
                print(vars(planet))

            print("Neutral planets:")
            for planet in gameinfo.neutral_planets.values():
                print(vars(planet))

            print("My planets:")
            for planet in gameinfo.my_planets.values():
                print(vars(planet))

            print("Enemy planets:")
            for planet in gameinfo.enemy_planets.values():
                print(vars(planet))

            print("Not my planets:")
            for planet in gameinfo.not_my_planets.values():
                print(vars(planet))

            print("All fleets:")
            for fleet in gameinfo.fleets.values():
                print(vars(fleet))  

            print("My fleets:")
            for fleet in gameinfo.my_fleets.values():
                print(vars(fleet))

            print("Enemy fleets:")
            for fleet in gameinfo.enemy_fleets.values():
                print(vars(fleet))

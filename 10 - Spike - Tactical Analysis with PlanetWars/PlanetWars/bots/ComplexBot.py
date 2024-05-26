class ComplexBot(object):

    def update(self, gameinfo):
        if not gameinfo:
            return

        my_planets = list(gameinfo.my_planets.values())
        neutral_planets = list(gameinfo.neutral_planets.values())
        enemy_planets = list(gameinfo.enemy_planets.values())

        self.scouting_mode(gameinfo, my_planets, neutral_planets, enemy_planets)

        self.attack_mode(gameinfo, my_planets, enemy_planets, neutral_planets)

    def scouting_mode(self, gameinfo, my_planets, neutral_planets, enemy_planets):
        for planet in my_planets:
            if planet.num_ships > 10:
                # Identify targets that need scouting
                scout_targets = sorted(neutral_planets + enemy_planets, key=lambda p: (p.vision_age, self.distance(planet, p)))[:3]
                for target in scout_targets:
                    if target.vision_age > 5:
                        # Send scouts using fleet_order
                        num_scouts = min(5, planet.num_ships - 10)
                        if num_scouts > 0:
                            gameinfo.fleet_order(planet, target, num_scouts)

    def attack_mode(self, gameinfo, my_planets, enemy_planets, neutral_planets):
        targets = sorted(enemy_planets + neutral_planets, key=lambda p: (p.growth_rate, p.num_ships), reverse=True)
        for planet in my_planets:
            for target in targets:
                if planet.num_ships > target.num_ships * 1.5:
                    # Send attack fleet using planet_order
                    num_ships_to_send = int(planet.num_ships * 0.75)
                    gameinfo.planet_order(planet, target, num_ships_to_send)
                    break

    def distance(self, planet1, planet2):
        return ((planet1.x - planet2.x)**2 + (planet1.y - planet2.y)**2)**0.5

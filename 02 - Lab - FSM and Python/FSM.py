import random

health = 20
enemy_health = 15
enemy_finder = 0
enemies_killed = 0

states = ['exploring', 'fighting', 'resting']
current_state = 'exploring'

alive = True
max_limit = 100
game_time = 0

while alive:
    game_time += 1

    if current_state == 'exploring':
        print("I am exploring for enemies to fight!")
        enemy_finder +=1

        if enemy_finder > 5:
            current_state = 'fighting'
            enemy_finder = 0
        
    if current_state == 'fighting':
        print("I am fighting a great beast!")
        health -= random.randint(1,4)
        enemy_health -= random.randint(1,4)

        if health <= 0:
            print("Game Over!: You died fighting a beast!")
            print(enemies_killed)
            end()
        if health < 3:
            current_state = "resting"
        if enemy_health <= 0:
            print("I have defeated the beast!")
            current_state = "exploring"
            enemies_killed += 1
            enemy_health = random.randint(7,15)

    if current_state == 'resting':
        print("I'm resting!")
        health += 4
        current_state = "exploring"

    if game_time > max_limit:
        print("Game Over! Time ran out!")
        print(enemies_killed)
        alive = False

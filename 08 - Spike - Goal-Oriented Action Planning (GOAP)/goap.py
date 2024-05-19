'''Goal Oriented Behaviour

Created for COS30002 AI for Games, Lab,
by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without
permission.

Works with Python 3+

Simple decision approach.
* Choose the most pressing goal (highest insistence value)
* Find the action that fulfills this "goal" the most (ideally?, completely?)

Goal: Eat (initially = 4)
Goal: Sleep (initially = 3)

Action: get raw food (Eat -= 3)
Action: get snack (Eat -= 2)
Action: sleep in bed (Sleep -= 4)
Action: sleep on sofa (Sleep -= 2)


Notes:
* This version is simply based on dictionaries and functions.

'''

VERBOSE = True

# Global goals with initial values
goals = {
    'Eat': 20,
    'Sleep': 16,
}

# Global (read-only) actions and effects
actions = {
    'get raw food': { 'Eat': -3, 'Sleep': 0 },
    'get snack': { 'Eat': -2, 'Sleep': 1 },
    'sleep in bed': { 'Sleep': -4, 'Eat': 1 },
    'sleep on sofa': { 'Sleep': -2, 'Eat': 1 }
}

def calcDiscontent(goals):
    '''Calculate the total discontent based on the current goal values.'''
    discontent = 0
    for value in goals.values():
        discontent += value * value
    return discontent

def apply_temp_action(action, temp_goals):
    '''Apply the action to the temp_goals without modifying the original goals.'''
    for goal, change in actions[action].items():
        temp_goals[goal] = max(temp_goals[goal] + change, 0)

def apply_action(action):
    '''Change all goal values using this action. An action can change multiple
    goals (positive and negative side effects).
    Negative changes are limited to a minimum goal value of 0.
    '''
    for goal, change in actions[action].items():
        goals[goal] = max(goals[goal] + change, 0)

def action_utility(action, goal):
    '''Return the 'value' of using "action" to achieve "goal".

    For example::
        action_utility('get raw food', 'Eat')

    returns a number representing the effect that getting raw food has on our
    'Eat' goal. Larger (more positive) numbers mean the action is more
    beneficial.
    '''
    ### Simple version - the utility is the change to the specified goal

    if goal in actions[action]:
        # Is the goal affected by the specified action?
        return -actions[action][goal]
    else:
        # It isn't, so utility is zero.
        return 0

    ### Extension
    ###
    ###  - return a higher utility for actions that don't change our goal past zero
    ###  and/or
    ###  - take any other (positive or negative) effects of the action into account
    ###    (you will need to add some other effects to 'actions')


def choose_action():
    assert len(goals) > 0, 'Need at least one goal'
    assert len(actions) > 0, 'Need at least one action'

    best_action = None
    lowest_discontent = None

    for key in actions.keys():
        temp_goals = goals.copy()
        apply_temp_action(key, temp_goals)
        current_discontent = calcDiscontent(temp_goals)

        if lowest_discontent is None or current_discontent < lowest_discontent:
            lowest_discontent = current_discontent
            best_action = key

    return best_action


#==============================================================================

def print_actions():
    print('ACTIONS:')
    # for name, effects in list(actions.items()):
    #     print(" * [%s]: %s" % (name, str(effects)))
    for name, effects in actions.items():
        print(" * [%s]: %s" % (name, str(effects)))


def run_until_all_goals_zero():
    HR = '-'*40
    print_actions()
    print('>> Start <<')
    print(HR)
    running = True
    while running:
        print('GOALS:', goals)
        # What is the best action
        action = choose_action()
        print('BEST ACTION:', action)
        # Apply the best action
        apply_action(action)
        print('NEW GOALS:', goals)
        # Stop?
        if all(value == 0 for goal, value in goals.items()):
            running = False
        print(HR)
    # finished
    print('>> Done! <<')


if __name__ == '__main__':
    # print(actions)
    # print(actions.items())
    # for k, v in actions.items():
    #     print(k,v)
    # print_actions()

    run_until_all_goals_zero()

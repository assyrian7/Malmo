import random

items=['pumpkin', 'sugar', 'egg', 'egg']
#1 3 6 6
#1 2 3 = 10
#1 3 4 = 13
#1 2 4 = 10
#2 3 4 = 15
#11
food_recipes = {'pumpkin_pie': ['pumpkin', 'egg', 'sugar'],
                'pumpkin_seeds': ['pumpkin']}

rewards_map = {'pumpkin': -5, 'egg': -25, 'sugar': -10,
               'pumpkin_pie': 100, 'pumpkin_seeds': -50}

def is_solution(reward):
    return reward == 0

def get_curr_state(items):
	item_m = {'pumpkin': 1, 'sugar': 3, 'egg': 6}
	total = 0
	for item in items:
		total = total + item_m[item]
    return total

def choose_action(curr_state, possible_actions, eps, q_table):
    rnd = random.random()
    a = random.randint(0, len(possible_actions) - 1)
    return possible_actions[a]
 
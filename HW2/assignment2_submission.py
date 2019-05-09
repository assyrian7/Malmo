import random

items=['pumpkin', 'sugar', 'egg', 'egg', 'red_mushroom', 'planks']
#1 3 6 6
#1 2 3 = 10
#1 3 4 = 13
#1 2 4 = 10
#2 3 4 = 15
#15
#65
'''
20 Showing best policy: sugar, pumpkin, egg, c_pumpkin_pie, present_gift,  with reward 100.0
Found solution
Done
'''
food_recipes = {'pumpkin_pie': ['pumpkin', 'egg', 'sugar'],
                'pumpkin_seeds': ['pumpkin'],
                'bowl': ['planks'],
                'mushroom_stew': ['bowl', 'red_mushroom']}

rewards_map = {'pumpkin': -5, 'egg': -25, 'sugar': -10,
               'pumpkin_pie': 100, 'pumpkin_seeds': -50, 'red_mushroom': 5, 'planks': -5, 'bowl': -1, 'mushroom_stew': 100}

def is_solution(reward):
    return reward == 200

def get_curr_state(items):
    item_m = {'pumpkin': 1, 'sugar': 3, 'egg': 9, 'pumpkin_seeds': 15, 'pumpkin_pie': 31, 'planks': 56, 'red_mushroom': 104, 'bowl': 197, 'mushroom_stew': 369}
    total = 0
    for item in items:
        total = total + item_m[item[0]]
    return total

def choose_action(curr_state, possible_actions, eps, q_table):
    rnd = random.random()
    a = ''
    #print(possible_actions)
    if(len(possible_actions) == 1):
        return possible_actions[0]
    if rnd <= eps:
        return possible_actions[random.randint(0, len(possible_actions) - 1)]
    else:
        actions = q_table[curr_state].items()
        #print(actions)
        q = -100
        ma = []
        col = 0
        i = 0
        for action in actions:
            #print(action)
            #print("a: " + str(i))
            if q_table[curr_state][action[0]] > q:
                a = action
                #print("b: " + str(i))
                q = q_table[curr_state][action[0]]
                ma.clear()
                ma.append(action)
                col = 1
            elif q_table[curr_state][action[0]] == q:
                col = col + 1
                ma.append(action)
            i+=1
        if col >= 2:
            #print(len(ma))
            i = random.randint(0, len(ma) - 1)
            #print("c: " + str(i))
            a = ma[i]
            while a[0] not in possible_actions:
                if len(ma) == 0:
                    return possible_actions[random.randint(0, len(possible_actions) - 1)]
                del ma[i]
                i = random.randint(0, len(ma) - 1)
                a = ma[i]
            #print(ma)
            #print("a: " + str(a))
        #print("State: " + str(curr_state))
        #print("Action: " + str(a[0]))
        return a[0]

'''
260 Showing best policy: red_mushroom, present_gift,  with reward 5.0
261 Learning Q-Table: red_mushroom, pumpkin, c_pumpkin_seeds, planks, c_bowl, present_gift, Reward: -46
262 Learning Q-Table: red_mushroom, present_gift, Reward: 5
263 Learning Q-Table: planks, pumpkin, red_mushroom, c_pumpkin_seeds, c_bowl, c_mushroom_stew, sugar, present_gift, Reward: 40
264 Learning Q-Table: red_mushroom, egg, planks, c_bowl, c_mushroom_stew, present_gift, Reward: 75
265 Showing best policy: red_mushroom, present_gift,  with reward 5.0
266 Learning Q-Table: red_mushroom, present_gift, Reward: 5
267 Learning Q-Table: red_mushroom, present_gift, Reward: 5
268 Learning Q-Table: red_mushroom, present_gift, Reward: 5
269 Learning Q-Table: red_mushroom, present_gift, Reward: 5
270 Showing best policy: red_mushroom, present_gift,  with reward 5.0
271 Learning Q-Table: red_mushroom, present_gift, Reward: 5
272 Learning Q-Table: red_mushroom, present_gift, Reward: 5
273 Learning Q-Table: red_mushroom, present_gift, Reward: 5
274 Learning Q-Table: red_mushroom, present_gift, Reward: 5
275 Showing best policy: red_mushroom, present_gift,  with reward 5.0
276 Learning Q-Table: red_mushroom, present_gift, Reward: 5
277 Learning Q-Table: red_mushroom, present_gift, Reward: 5
278 Learning Q-Table: red_mushroom, present_gift, Reward: 5
279 Learning Q-Table: red_mushroom, pumpkin, present_gift, Reward: 0
280 Showing best policy: red_mushroom, present_gift,  with reward 5.0
'''
 
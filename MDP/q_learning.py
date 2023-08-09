from uncertain_grid import Uncertain_Grid
import random
import math
import operator


def add_new_state_to_q_table(instance, q_table, state):
    """
    Adds a new state if this is the first time we have reached it
    :param instance: object of the class Uncertain Grid
    :param q_table: Nested dictionary in the form (state:{action: q_value}}
    :param state: new_state that does not exist in the dictionary (x,y)
    :return:
    """
    if instance.is_episode_over():
        reward = 100
        q_table[state] = {'north': reward, 'south': reward, 'east': reward, 'west': reward}
    else:
        q_table[state] = {'north': 0, 'south': 0, 'east': 0, 'west': 0}
    return q_table


def max_q_value_for_state(q_table, state):
    """
    :return: int - the max q_table value for the state
    """
    return max(list(q_table[state].values()))


def update_q_table(q_table, cur_state, new_state, action, reward, learning_rate):
    """
    ******HINT : You can use the max_q_value_for_state function
    :param q_table: Nested dictionary in the form (state:{action: q_value}} to update
    :param cur_state: The state before performing action (x,y)
    :param new_state: The state after performing action (x,y)
    :param action: The action we attempted ('north','south'...)
    :param reward: reward (int)
    :param learning_rate: learning rate (int)
    :return: updated q table based on the new state
    """
    q_table[cur_state][action] = (1-learning_rate) * q_table[cur_state][action] + learning_rate * (reward + max_q_value_for_state(q_table, new_state))
    return q_table


def choose_action_to_execute(q_table, current_state):
    """
    :param q_table: Nested dictionary in the form (state:{action: q_value}} to update
    :param current_state: The current state on the grid (x,y)
    :return: action to perform from : ['north', 'south', 'east' or 'west']
    """
    best_action = max(q_table[current_state], key=q_table[current_state].get)
    exploration_rate = 0.5  # The probability to exploit, please make sure the value is 0.5 when submitting!
    if random.uniform(0, 1) > exploration_rate:  # HINT: Explore or exploit?
        action = random.choice(['north', 'south', 'east', 'west'])
        while action == best_action:
            action = random.choice(['north', 'south', 'east', 'west'])
    else:
        action = best_action
    return action



def get_policy(instance, q_table):
    """
    :param instance: instance of the problem
    :param q_table: latest q_table
    :return: Dictionary of policy in the form: (x,y): 'direction'
    """
    policy = instance.create_policy_array()  # Init with all states points to 'south'
    for state in policy.keys():  # For each s in S
        if state in policy:
            policy[state] = max(q_table[state], key=q_table[state].get)
    return policy


def q_learning(instance, learning_rate=0.01, num_episodes=10000):
    """
    :param instance: instance of the problem (Uncertain_Grid object)
    :param num_episodes: number of episodes for q-learning updates (int)
    :param learning_rate: the learning rate parameter (int)
    :return:
    """
    q_table = {}
    q_table = add_new_state_to_q_table(instance, q_table, instance.current_state)
    while num_episodes > 0:
        cur_state = instance.current_state
        action = choose_action_to_execute(q_table, instance.current_state)
        new_state, reward = instance.execute_action(action)
        if new_state not in q_table.keys():  # If we have reached a new state for the first time
            q_table = add_new_state_to_q_table(instance, q_table, new_state)
        # update_q_table function below needs to be implemented by the student
        q_table = update_q_table(q_table, cur_state, new_state, action, reward, learning_rate)
        if instance.is_episode_over():  # If we have reached the end state
            instance.new_episode()
            num_episodes -= 1
    print(q_table)
    return get_policy(instance, q_table)



# from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product
import copy
import math


class TicTacToe():

    def __init__(self):
        """initialise the board"""
        
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix

        self.reset()


    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        if (curr_state[0]+curr_state[1]+curr_state[2])==15:
            return True
        elif (curr_state[3]+curr_state[4]+curr_state[5])==15:
            return True
        elif (curr_state[6]+curr_state[7]+curr_state[8])==15:
            return True
        elif (curr_state[0]+curr_state[3]+curr_state[6])==15:
            return True
        elif (curr_state[1]+curr_state[4]+curr_state[7])==15:
            return True
        elif (curr_state[2]+curr_state[5]+curr_state[8])==15:
            return True
        elif (curr_state[0]+curr_state[4]+curr_state[8])==15:
            return True
        elif (curr_state[2]+curr_state[4]+curr_state[6])==15:
            return True
        else:
            return False
        
 

    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up

        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) == 0:
            return True, 'Tie'

        else:
            return False, 'Resume'


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]

        return (agent_values, env_values)


    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""

        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        return (agent_actions, env_actions)



    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        retn = copy.deepcopy(curr_state)
        retn[curr_action[0]] = curr_action[1]
        return retn


    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""
#         print(curr_state)
        curr_state = self.state_transition(curr_state, curr_action)
#         print(curr_state)
        is_term = self.is_terminal(curr_state)
#         print(is_term[0])
        term = False
        if is_term[0]==True and is_term[1]=='Win':
            reward = 100
            term = True
        elif is_term[0]==True and is_term[1]=='Tie':
            reward = 0
            term = True
        else:
            reward = -1
            
        if is_term[0] == False:    
            itert = np.random.choice(len(list(self.action_space(curr_state)[1])))
            ns = self.state_transition(curr_state, list(self.action_space(curr_state)[1])[itert])
#             print(ns)
            
            is_term1 = self.is_terminal(ns)
        
            if is_term1[0]==True and is_term1[1]=='Win':
                reward += -100
                term = True

        if is_term[0]==False:
            ret_ns = ns
            
        else:
            ret_ns = curr_state

        return (ret_ns, reward, term)
        
          


    def reset(self):
        return self.state

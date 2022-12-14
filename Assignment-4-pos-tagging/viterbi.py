"""
Viterbi Algorithm for inferring the most likely sequence of states from an HMM.

Patrick Wang, 2021
"""
import math
import numpy as np

def viterbi(observations, transition_frequency, emission_frequency):
    # Intital variable set up
    possible_pos_states = []
    possible_pos_freq = []
    all_states = get_all_states(transition_frequency)
    
    # Calculate the observation probabilities using Transition and Emission frequencies
    for index, word in enumerate(observations):        
        word = word.lower()
        if index == 0: # For the initial state, calculate all state probabilities
            for state in all_states:
                emission_prob = emission_frequency[word][state]
                state_frequency = np.log(transition_frequency['START'][state]*emission_prob)
                possible_pos_states.append([state])
                possible_pos_freq.append([state_frequency])
    
        else: # For following states, calculate the 'max' probabable state based on prior/prev state
            for index in range(len(possible_pos_states)):
                prev_state = possible_pos_states[index][-1]
                prev_freq = possible_pos_freq[index][0]
                max_freq = -math.inf
                for state in all_states:
                    emission_prob = emission_frequency[word][state]
                    temp_freq = np.log(transition_frequency[prev_state][state]*emission_prob)
                    if temp_freq*prev_freq > max_freq:
                        max_freq = temp_freq*prev_freq
                        max_state = state
                possible_pos_states[index].append(max_state)
                possible_pos_freq[index][0] = max_freq
    
    max_index = np.argmax(possible_pos_freq)
    return possible_pos_states[max_index]

def get_all_states(transition_frequency):
    all_states = set()
    for key in transition_frequency.keys():
        all_states.add(key)
        for key_ in transition_frequency[key].keys():
            all_states.add(key_)
    return list(all_states)

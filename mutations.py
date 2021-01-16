import numpy as np
import utils
#from bisect import bisect_left, bisect_right

'''
    Assume that there is always at least 2 notes in the vector
'''
INTERVAL_POSSIBLE_CHANGES = [i for i in range(-12, 13)]
def modify_note_within_interval(note, probs):
    '''
    Return the note changed randomly within the interval
    '''
    if probs == 'uniform':
        change = np.random.choice(INTERVAL_POSSIBLE_CHANGES)
    else:
        change = np.random.choice(INTERVAL_POSSIBLE_CHANGES, p=probs)
    return min(max(note + change, 0), 127) 

def single_note_transposition(gen_vec, probs='uniform'):
    '''
    Change the pitch of a selected note by a random interval within one octave
    '''
    notes_mask = gen_vec >= 0
    if notes_mask.sum() == 0:
        return gen_vec
    note_to_change = np.random.choice(notes_mask.nonzero()[0])
    old_value = gen_vec[note_to_change]
    
    gen_vec[note_to_change] = modify_note_within_interval(old_value, probs)
    return gen_vec

def interval_mutation(gen_vec, probs='uniform'):
    '''
    change the interval between two consecutive notes to another within one octave
    '''
    notes_mask = gen_vec >= 0
    n = notes_mask.sum() - 1
    if n <= 0:
        return gen_vec
    pair_to_change = np.random.randint(0, n)
        
    val1 = gen_vec[notes_mask][pair_to_change]
    val2 = gen_vec[notes_mask][pair_to_change + 1]
    mode = np.random.randint(0, 2)
    if mode:
        gen_vec[notes_mask.nonzero()[0][pair_to_change]] = modify_note_within_interval(val2, probs)
    else:
        gen_vec[notes_mask.nonzero()[0][pair_to_change + 1]] = modify_note_within_interval(val1, probs)
    return gen_vec

def note_position_mutation(gen_vec):
    #instead of note prolongation mutation
    '''
    change the positions of two selected notes or rests (pauses) by moving 
    a rest or note in the vector (1 position to the left or 1 position to the right)
    '''
    notes_mask = gen_vec != -2
    note_to_move = np.random.choice(notes_mask.nonzero()[0])
    mode = np.random.choice([-1, 1])
    if note_to_move + mode != len(gen_vec) and note_to_move + mode != -1:
        note_val = gen_vec[note_to_move]
        gen_vec[note_to_move] = gen_vec[note_to_move + mode]
        gen_vec[note_to_move + mode] = note_val
    return gen_vec

def rest_to_note_mutation(gen_vec, probs='uniform'):
    #instead of rests_to_notes_ratio_mutation
    '''
    change randomly chosen rest to a note with value within ocatave to ones 
    of rests' neighbour
    '''
    rests_mask = gen_vec == -1
    if rests_mask.sum() == 0: 
        return gen_vec
    notes_mask = gen_vec >= 0
    rest_to_change = np.random.choice(rests_mask.nonzero()[0])
    neigbour_candidates = notes_mask.nonzero()[0]
    mode = np.random.randint(0, 2)
    #TODO: use bisect below of sth to have O(logn) and not O(n)
    if mode:
        neighbours_mask = neigbour_candidates > rest_to_change
    else:
        neighbours_mask = neigbour_candidates < rest_to_change
    if not neighbours_mask.any():
        neighbours_mask = ~neighbours_mask & neigbour_candidates != rest_to_change
    neigbour_candidates = neigbour_candidates[neighbours_mask] 
    if not len(neigbour_candidates):
        gen_vec[rest_to_change] = np.random.randint(0, 128)
    else:
        neighbour_note = min(neigbour_candidates, key=lambda x: abs(x-rest_to_change))
        gen_vec[rest_to_change] = modify_note_within_interval(gen_vec[neighbour_note], probs)
    return gen_vec

def note_to_rest_mutation(gen_vec):
    #instead of rests_to_notes_ratio_mutation
    '''
    change randomly chosen note to a rest 
    '''
    notes_mask = gen_vec >= 0
    note_to_change = np.random.choice(notes_mask.nonzero()[0])
    gen_vec[note_to_change] = -1
    return gen_vec

def note_to_prolongation_mutation(gen_vec):
    #instead of rythmic mutation
    notes_mask = gen_vec != -2
    note_to_change = np.random.randint(1, notes_mask.sum())
    note_idx = notes_mask.nonzero()[0][note_to_change]
    gen_vec[note_idx] = -2
    return gen_vec

def prolongation_to_note_mutation(gen_vec):
    #TODO
    #instead of rythmic mutation
    notes_mask = gen_vec == -2
    note_to_change = np.random.randint(1, notes_mask.sum())
    note_idx = notes_mask.nonzero()[0][note_to_change]
    gen_vec[note_idx] = -2
    return gen_vec
    
if __name__ == '__main__':

    for i in range(10000):
        gen_representation = utils.generate_music_vector(np.random.randint(4, 100))
        repr_mutated = single_note_transposition(gen_representation.copy())
        assert((gen_representation == repr_mutated).sum() >= len(gen_representation) - 1) # changed on 1 position or haven't changed
        assert(((gen_representation == -2) == (repr_mutated == -2)).all()) # pronongations haven't changed
        assert(((gen_representation == -1) == (repr_mutated == -1)).all()) # pauses haven't changed
        
        repr_mutated = interval_mutation(gen_representation.copy())
        assert((gen_representation == repr_mutated).sum() >= len(gen_representation) - 1) # changed on 1 position or haven't changed
        assert(((gen_representation == -2) == (repr_mutated == -2)).all()) # pronongations haven't changed
        assert(((gen_representation == -1) == (repr_mutated == -1)).all()) # pauses haven't changed
        
        repr_mutated = note_position_mutation(gen_representation.copy())
        assert((gen_representation == repr_mutated).sum() == len(gen_representation) - 2 or
               (gen_representation == repr_mutated).sum() == len(gen_representation)) # changed on 2 positions or haven't changed
        assert((gen_representation == -2).sum() == (repr_mutated == -2).sum()) # number of pronongations haven't changed
        assert((gen_representation == -1).sum() == (repr_mutated == -1).sum()) # number of pauses haven't changed
        assert((gen_representation >= 0).sum() == (repr_mutated >= 0).sum()) # number of notes haven't changed
        
        repr_mutated = rest_to_note_mutation(gen_representation.copy())
        if not (gen_representation == -1).sum():
            assert((repr_mutated == gen_representation).all()) # nothing have changed
        else:
            assert((gen_representation == repr_mutated).sum() == len(gen_representation) - 1) # changed on 1 position
            assert((gen_representation == -2).sum() == (repr_mutated == -2).sum()) # number of pronongations haven't changed
            assert((gen_representation == -1).sum() == (repr_mutated == -1).sum() + 1) # number of pauses have decreased by 1
            assert((gen_representation >= 0).sum() == (repr_mutated >= 0).sum() - 1) # number of notes have increased by 1
        '''
        
        repr_mutated5 = rythmic_mutation(gen_representation.copy())
        assert((gen_representation == repr_mutated5).sum() == len(gen_representation) - 1) # changed on 1 position
        assert(abs((gen_representation == -2).sum() - (repr_mutated5 == -2).sum()) == 1)
        '''
import numpy as np
import utils
import representations
#from bisect import bisect_left, bisect_right

###############################################################################
###################################UTILS#######################################
###############################################################################

INTERVAL_POSSIBLE_CHANGES = np.array([i for i in range(-12, 13)])
def modify_note_within_interval(note, probs, change_not_zero=True):
    '''
    Return the note changed randomly within the interval
    '''
    
    mask_result_below_max = INTERVAL_POSSIBLE_CHANGES + note < 128
    mask_result_above_min = INTERVAL_POSSIBLE_CHANGES + note >= 0
    mask = mask_result_below_max & mask_result_above_min
    if change_not_zero:
        mask_change_not_zero = INTERVAL_POSSIBLE_CHANGES != 0
        mask = mask & mask_change_not_zero
        
    possible_changes = INTERVAL_POSSIBLE_CHANGES[mask]
    if probs == 'uniform':
        change = np.random.choice(possible_changes)
    else:
        change = np.random.choice(possible_changes, p=probs[mask])
    return note + change

def masked_to_note_mutation(gen_vec, mask_to_change, probs):
    if not mask_to_change.any(): 
        return gen_vec
    mask_notes = gen_vec >= 0
    pos_to_change = np.random.choice(mask_to_change.nonzero()[0])
    neigbour_candidates = mask_notes.nonzero()[0]
    mode = np.random.randint(0, 2)
    #TODO: use bisect below of sth to have O(logn) and not O(n)
    if mode:
        neighbours_mask = neigbour_candidates > pos_to_change
    else:
        neighbours_mask = neigbour_candidates < pos_to_change
    if not neighbours_mask.any():
        neighbours_mask = ~neighbours_mask & neigbour_candidates != pos_to_change
    neigbour_candidates = neigbour_candidates[neighbours_mask] 
    if not len(neigbour_candidates):
        gen_vec[pos_to_change] = np.random.randint(0, 128)
    else:
        neighbour_note = min(neigbour_candidates, key=lambda x: abs(x-pos_to_change))
        gen_vec[pos_to_change] = modify_note_within_interval(gen_vec[neighbour_note], probs)
    return gen_vec
###############################################################################
#################################MUTATIONS#####################################
###############################################################################

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
        gen_vec[notes_mask.nonzero()[0][pair_to_change]] = modify_note_within_interval(val2, probs, change_not_zero=False)
    else:
        gen_vec[notes_mask.nonzero()[0][pair_to_change + 1]] = modify_note_within_interval(val1, probs, change_not_zero=False)
    return gen_vec

def note_position_mutation(gen_vec):
    #instead of note prolongation mutation
    '''
    change the rhythm values of two notes or rests (rests) by moving 
    a rest or note in the vector (1 position to the left or 1 position to the right)
    '''
    notes_mask = gen_vec != -2
    if notes_mask.sum() < 2:
        return gen_vec
    
    possible_notes = notes_mask.nonzero()[0]
    note_to_move = np.random.choice(possible_notes)
    mode = np.random.choice([-1, 1])
    if gen_vec[1] == -2 and (note_to_move + mode == 0 or note_to_move == 0):
        note_to_move = possible_notes[1]
    if note_to_move + mode == len(gen_vec) or note_to_move + mode == -1:
        mode = -mode
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
    return masked_to_note_mutation(gen_vec, rests_mask, probs)

def note_to_rest_mutation(gen_vec):
    #instead of rests_to_notes_ratio_mutation
    '''
    change randomly chosen note to a rest 
    '''
    notes_mask = gen_vec >= 0
    if not notes_mask.any():
        return gen_vec
    note_to_change = np.random.choice(notes_mask.nonzero()[0])
    gen_vec[note_to_change] = -1
    return gen_vec

def note_to_prolongation_mutation(gen_vec):
    #instead of rhythmic mutation
    '''
    change randomly chosen note to a prolongation
    '''
    notes_mask = gen_vec >= 0
    candidates = notes_mask.nonzero()[0]
    candidates = candidates[candidates != 0] # first element can't be prolongation
    if not len(candidates):
        return gen_vec
    note_to_change = np.random.choice(candidates)
    gen_vec[note_to_change] = -2
    return gen_vec

def prolongation_to_note_mutation(gen_vec, probs='uniform'):
    #instead of rhythmic mutation
    '''
    change randomly chosen prolongation to a note
    '''
    prolongation_mask = gen_vec == -2
    return masked_to_note_mutation(gen_vec, prolongation_mask, probs)

def long_to_short_ratio_mutation(gen_vec):
    '''
    prolongs randomly chosen note if classified as short, and divides into 2 notes
    if classified as long
    '''
    mask = gen_vec != -2
    candidates = mask.nonzero()[0]
    midi_repr, durations = representations.gen_to_midi(gen_vec)
    note_to_change = np.random.randint(0, len(midi_repr))
    duration = durations[note_to_change]
    note_to_change = candidates[note_to_change]
    
    if duration < 4:
        if note_to_change > len(gen_vec) - 4:
            gen_vec[-4] = gen_vec[note_to_change]
            note_to_change = len(gen_vec) - 4
        gen_vec[note_to_change + 1: note_to_change + 4] = -2
    else:
        gen_vec[note_to_change + duration // 2] = gen_vec[note_to_change]
        
    return gen_vec
    
    
if __name__ == '__main__':

    for i in range(10000):
        gen_representation = utils.generate_music_vector(np.random.randint(4, 100))
        repr_mutated = single_note_transposition(gen_representation.copy())
        if (gen_representation < 0).all():
            assert((repr_mutated == gen_representation).all()) # nothing have changed
        else:
            assert((gen_representation == repr_mutated).sum() == len(gen_representation) - 1) # changed on 1 position
            assert(((gen_representation == -2) == (repr_mutated == -2)).all()) # pronongations haven't changed
            assert(((gen_representation == -1) == (repr_mutated == -1)).all()) # rests haven't changed
            
        repr_mutated = interval_mutation(gen_representation.copy())
        assert((gen_representation == repr_mutated).sum() >= len(gen_representation) - 1) # changed on 1 position or haven't changed
        assert(((gen_representation == -2) == (repr_mutated == -2)).all()) # pronongations haven't changed
        assert(((gen_representation == -1) == (repr_mutated == -1)).all()) # rests haven't changed
        
        repr_mutated = note_position_mutation(gen_representation.copy())
        assert((gen_representation == repr_mutated).sum() == len(gen_representation) - 2 or
               (gen_representation == repr_mutated).sum() == len(gen_representation)) # changed on 2 positions or haven't changed
        assert((gen_representation == -2).sum() == (repr_mutated == -2).sum()) # number of pronongations haven't changed
        assert((gen_representation == -1).sum() == (repr_mutated == -1).sum()) # number of rests haven't changed
        assert((gen_representation >= 0).sum() == (repr_mutated >= 0).sum()) # number of notes haven't changed
        
        repr_mutated = rest_to_note_mutation(gen_representation.copy())
        if not (gen_representation == -1).any():
            assert((repr_mutated == gen_representation).all()) # nothing have changed
        else:
            assert((gen_representation == repr_mutated).sum() == len(gen_representation) - 1) # changed on 1 position
            assert((gen_representation == -2).sum() == (repr_mutated == -2).sum()) # number of pronongations haven't changed
            assert((gen_representation == -1).sum() == (repr_mutated == -1).sum() + 1) # number of rests have decreased by 1
            assert((gen_representation >= 0).sum() == (repr_mutated >= 0).sum() - 1) # number of notes have increased by 1
        
        repr_mutated = note_to_rest_mutation(gen_representation.copy())
        if not (gen_representation >= 0).any():
            assert((repr_mutated == gen_representation).all()) # nothing have changed
        else:
            assert((gen_representation == repr_mutated).sum() == len(gen_representation) - 1) # changed on 1 position
            assert((gen_representation == -2).sum() == (repr_mutated == -2).sum()) # number of pronongations haven't changed
            assert((gen_representation == -1).sum() == (repr_mutated == -1).sum() - 1) # number of rests have increased by 1
            assert((gen_representation >= 0).sum() == (repr_mutated >= 0).sum() + 1) # number of notes have decreased by 1
        
        repr_mutated = note_to_prolongation_mutation(gen_representation.copy())
        candidates = (gen_representation >= 0).nonzero()[0]
        candidates = candidates[candidates != 0] # first element can't be prolongation
        if not len(candidates):
            assert((repr_mutated == gen_representation).all()) # nothing have changed
        else:
            assert((gen_representation == repr_mutated).sum() == len(gen_representation) - 1) # changed on 1 position
            assert((gen_representation == -2).sum() == (repr_mutated == -2).sum() - 1) # number of pronongations have increased by 1
            assert((gen_representation == -1).sum() == (repr_mutated == -1).sum()) # number of rests haven't changed 1
            assert((gen_representation >= 0).sum() == (repr_mutated >= 0).sum() + 1) # number of notes have decreased by 1
        
        repr_mutated = prolongation_to_note_mutation(gen_representation.copy())
        if not (gen_representation == -2).any():
            assert((repr_mutated == gen_representation).all()) # nothing have changed
        else:
            assert((gen_representation == repr_mutated).sum() == len(gen_representation) - 1) # changed on 1 position
            assert((gen_representation == -2).sum() == (repr_mutated == -2).sum() + 1) # number of pronongations have increased by 1
            assert((gen_representation == -1).sum() == (repr_mutated == -1).sum()) # number of rests haven't changed
            assert((gen_representation >= 0).sum() == (repr_mutated >= 0).sum() - 1) # number of notes have increased by 1

        repr_mutated = long_to_short_ratio_mutation(gen_representation.copy())
        midi_repr, durations = representations.gen_to_midi(gen_representation)
        midi_mutated_repr, durations_mutated = representations.gen_to_midi(repr_mutated)
        assert((repr_mutated != gen_representation).any()) # sth have changed
        assert(durations_mutated != durations) # durations have changed
import pandas as pd

def create_notes_to_midi_mapping():
    notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    temp = []
    for n in notes:
        temp.append(n)
        if n not in ('E', 'B'):
            temp.append(n + '#')
            
    notes = temp
    
    octaves = list(range(-1, 10))
    temp = []
    
    for o in octaves:
        #postfix = ('+' if o >= 0 else '') + str(o)
        for n in notes:
            if o != 9 or n not in ('G#', 'A', 'A#', 'B'):
                temp.append(n + str(o))
                
    notes_to_pitches_dict = {note: value for (value, note) in enumerate(temp)}
    return notes_to_pitches_dict

def midi_to_notes(vec):
    midi_dict = create_notes_to_midi_mapping()
    midi_dict = dict((v, k) for k, v in midi_dict.items())
    return [midi_dict[i] for i in vec]

def notes_to_midi(vec):
    midi_dict = create_notes_to_midi_mapping()
    return [midi_dict[i] for i in vec]

def gen_to_midi(vec):
    midi_vec = []
    midi_durations = []
    duration_counter = 0
    for n in vec:
        if n != -2:
            midi_vec.append(n)
            if duration_counter:
                midi_durations.append(duration_counter)
            duration_counter = 1
        else:
            duration_counter += 1
    midi_durations.append(duration_counter)
    return midi_vec, midi_durations

def midi_to_gen(midi_vec, midi_durations):
    gen_representation = []
    for note, duration in zip(midi_vec, midi_durations):
        gen_representation.append(note)
        gen_representation += [-2] * (duration - 1)
    return gen_representation

if __name__ == '__main__':
    midi_dict = create_notes_to_midi_mapping()
    degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
    notes_representation = midi_to_notes(degrees)
    midi_representation = notes_to_midi(notes_representation)
    assert(midi_representation == degrees)
    
    gen_representation = [60, -2, -2, -2, 62, -2, -2, -2, 64, -2, -2, -2, 65, -2, -2, -2,
                          67, -2, -2, -2, 69, -2, -2, -2, 71, -2, -2, -2, 72, -2, -2, -2,
                          -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2,
                          72, -2, -2, -2, 71, -2, -2, -2, 69, -2, -2, -2, 67, -2, -2, -2,
                          65, -2, -2, -2, 64, -2, -2, -2, 62, -2, -2, -2, 60, -2, -2, -2]
    
    midi_representation, midi_durations = gen_to_midi(gen_representation)
    assert(midi_representation == degrees + [-1] + list(reversed(degrees)))
    assert(midi_durations == [4] * len(degrees) + [16] + [4] * len(degrees))
    
    g_repr = midi_to_gen(midi_representation, midi_durations)
    assert(g_repr == gen_representation)
    
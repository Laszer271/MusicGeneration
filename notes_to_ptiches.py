import pandas as pd
import pypianoroll

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

if __name__ == '__main__':
    midi_dict = create_notes_to_midi_mapping()
    degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
    notes_representation = midi_to_notes(degrees)
    midi_representation = notes_to_midi(notes_representation)
    assert(midi_representation == degrees)
    
    paths = pd.read_csv('1_track_songs_dataset.csv')['Path']
    song = pypianoroll.read(paths[0])
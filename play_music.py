import numpy as np
from evolution.utils import representations
from midiutil import MIDIFile
from evolution.utils import play_midi

def play_music(pitches, durations):
    track    = 0
    channel  = 0
    time     = 0    # In beats
    tempo    = 200   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard
    
    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                          # automatically)
    MyMIDI.addTempo(track, time, tempo)
    
    for pitch, duration in zip(pitches, durations):
        if pitch != -1:
            MyMIDI.addNote(track, channel, pitch, time, duration, volume)
        time += duration
        
    music_file = 'generated_song.mid'
    with open(music_file, 'wb') as output_file:
        MyMIDI.writeFile(output_file)
    
    play_midi.play_music(music_file)

if __name__ == '__main__':
    songs = np.load('generated_songs.npy')
    for i, song in enumerate(songs):
        pitches, durations = representations.gen_to_midi(song)
        print('Music nr:', i)
        print('Notes:')
        pitches = np.array(pitches)
        pitches = pitches[pitches >= 0]
        pitches_notes = representations.midi_to_notes(pitches)
        print(pitches_notes)
        play_music(pitches, durations)
        print('Press enter to continue:', end='')
        input()
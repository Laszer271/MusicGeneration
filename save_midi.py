from midiutil import MIDIFile
import play_midi

degrees  = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI note number
#durations = [4, 4, 4, 4, 4, 4, 4, 4]
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 480   # In BPM
volume   = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(degrees):
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

for i, pitch in enumerate(reversed(degrees)):
    MyMIDI.addNote(track, channel, pitch, time + i + len(degrees), duration, volume)

music_file = 'major-scale.mid'
with open(music_file, 'wb') as output_file:
    MyMIDI.writeFile(output_file)

play_midi.play_music(music_file)
import pandas as pd
import play_midi

df = pd.read_csv('1_track_songs_dataset.csv')
paths = df['Path']

for path in paths:
    play_midi.play_music(path, volume=0.1)
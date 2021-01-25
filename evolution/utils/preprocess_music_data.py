import os
import collections
import six
import pypianoroll
import pandas as pd
import numpy as np

def is_iterable(arg):
    return (
        isinstance(arg, collections.Iterable) 
        and not isinstance(arg, six.string_types)
    )

def get_images_paths(input_path):
    final_images_paths = []
    
    items = []
    temp_items = []

    if is_iterable(input_path):
        temp_items.extend(input_path)
    else:
        temp_items.append(input_path)
    
    while len(temp_items):
        items = temp_items
        temp_items = []
        
        for item in items:
            if not item.endswith('.mid'):
                # we assume that item is actually a directory
                try:
                    new_items = os.listdir(item)
                    for new_item in new_items:
                        temp_items.append(item + f'/{new_item}')
                except NotADirectoryError:
                    pass
            else:
                final_images_paths.append(item)
    
    return final_images_paths

path = 'data/midi-classic-music'
paths = get_images_paths(path)
df = pd.DataFrame({'Path': paths})
df['Name'] = df['Path'].str.extract('(?<=\/)([^\/]+\.mid)')
df = df.drop_duplicates(subset='Name')

tracks_numbers = []
for path in df['Path']:
    try:
        m = pypianoroll.read(path)
        tracks = list(m)
        tracks_numbers.append(len(tracks))
    except:
        tracks_numbers.append(np.nan)

df['N_Tracks'] = tracks_numbers
df.to_csv('songs_dataset.csv', index=False)
#get the songs that have only one track
df_1_track = df[df['N_Tracks'] == 1]
df_1_track.to_csv('1_track_songs_dataset.csv', index=False)

import numpy as np
from .utils import utils


def generate_music_vectors(song_size=16, population_size=1, probabilities=None):
    songs = []
    for i in range(population_size):
        song = np.random.choice(utils.POSSIBLE_VALUES, song_size, p=probabilities)
        while song[0] == -2:
            song[0] = np.random.choice(utils.POSSIBLE_VALUES, p=probabilities)
        songs.append(song)
    return songs
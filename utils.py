import numpy as np

POSSIBLE_VALUES = range(-2, 128)
PROLONGATION_VALUE = -2
REST_VALUE = -1
NOTE_VALUES = range(0, 128)

LOWEST_PITCH = 0 # has to be C for proper key defining
HIGHEST_PITCH = 127
OCTAVE_LENGTH = 12
FULL_OCTAVES_NO = int(np.floor(HIGHEST_PITCH / OCTAVE_LENGTH))

PROLONGATION_WEIGHT = 0.5
PAUSE_WEIGHT = 0.05
WEIGHTS = [(1.0-PROLONGATION_WEIGHT-PAUSE_WEIGHT)/128.0  for i in range(128)]
WEIGHTS = [PROLONGATION_WEIGHT, PAUSE_WEIGHT] + WEIGHTS
def generate_music_vector(n):
    song = np.random.choice(POSSIBLE_VALUES, n, p=WEIGHTS)
    while song[0] == -2:
        song[0] = np.random.choice(POSSIBLE_VALUES, p=WEIGHTS)
    return song

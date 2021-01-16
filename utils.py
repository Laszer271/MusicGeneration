import numpy as np

POSSIBLE_VALUES = range(-2, 128)
PROLONGATION_WEIGHT = 0.5
PAUSE_WEIGHT = 0.05
WEIGHTS = [(1.0-PROLONGATION_WEIGHT-PAUSE_WEIGHT)/128.0  for i in range(128)]
WEIGHTS = [PROLONGATION_WEIGHT, PAUSE_WEIGHT] + WEIGHTS
def generate_music_vector(n):
    song = np.random.choice(POSSIBLE_VALUES, n, p=WEIGHTS)
    while song[0] == -2:
        song[0] = np.random.choice(POSSIBLE_VALUES, p=WEIGHTS)
    return song
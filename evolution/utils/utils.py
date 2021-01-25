import numpy as np

OCTAVE_LENGTH = 12
MINOR_SECOND_INTERVAL = 1
MAJOR_SECOND_INTERVAL = 2
TRITONE_INTERVAL = 6
MINOR_SEVENTH_INTERVAL = 10
MAJOR_SEVENTH_INTERVAL = 11
DISSONANCES = [MINOR_SECOND_INTERVAL, MAJOR_SECOND_INTERVAL, TRITONE_INTERVAL, MINOR_SEVENTH_INTERVAL, MAJOR_SEVENTH_INTERVAL]

POSSIBLE_VALUES = range(-2, 128)
PROLONGATION_VALUE = -2
REST_VALUE = -1
NOTE_VALUES = range(0, 128)

LOWEST_PITCH = 0 # has to be C for proper key defining
HIGHEST_PITCH = 127
FULL_OCTAVES_NO = int(np.floor(HIGHEST_PITCH / OCTAVE_LENGTH))

PROLONGATION_PROB = 0.5
REST_PROB = 0.05
PROBS = [(1.0-PROLONGATION_PROB-REST_PROB)/128.0  for i in range(128)]
PROBS = [PROLONGATION_PROB, REST_PROB] + PROBS
def generate_music_vector(n):
    song = np.random.choice(POSSIBLE_VALUES, n, p=PROBS)
    while song[0] == -2:
        song[0] = np.random.choice(POSSIBLE_VALUES, p=PROBS)
    return song

def get_intervals(gen_vec):
    notes = gen_vec[gen_vec >= LOWEST_PITCH]
    return np.abs(notes[1:] - notes[:-1])

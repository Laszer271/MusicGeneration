import numpy as np
from . import utils

MAJOR_INTERVALS = [0, 2, 4, 5, 7, 9, 11]
MINOR_INTERVALS = [0, 2, 3, 5, 7, 8, 10]

# set of scales in defined mode
def major_mode(note):
    scale = [note + interval for interval in MAJOR_INTERVALS]
    return scale
def minor_mode(note):
    scale = [note + interval for interval in MINOR_INTERVALS]
    return scale

# set of notes in key
def generate_key(starting_note, mode):
    key = []
    for octave in range(0, utils.FULL_OCTAVES_NO - 1):
        key.extend( mode(starting_note + utils.OCTAVE_LENGTH * octave) )
    unfull_octave = np.array( mode(starting_note + utils.OCTAVE_LENGTH * utils.FULL_OCTAVES_NO) )
    key.extend(unfull_octave[unfull_octave <= utils.HIGHEST_PITCH])
    return key

# defined keys
# major
C_MAJOR = generate_key(0, major_mode)
Db_MAJOR = generate_key(1, major_mode)
D_MAJOR = generate_key(2, major_mode)
Eb_MAJOR = generate_key(3, major_mode)
E_MAJOR = generate_key(4, major_mode)
F_MAJOR = generate_key(5, major_mode)
Gb_MAJOR = generate_key(6, major_mode)
G_MAJOR = generate_key(7, major_mode)
Ab_MAJOR = generate_key(8, major_mode)
A_MAJOR = generate_key(9, major_mode)
Bb_MAJOR = generate_key(10, major_mode)
B_MAJOR = generate_key(11, major_mode)
# minor
C_MINOR = generate_key(0, minor_mode)
Db_MINOR = generate_key(1, minor_mode)
D_MINOR = generate_key(2, minor_mode)
Eb_MINOR = generate_key(3, minor_mode)
E_MINOR = generate_key(4, minor_mode)
F_MINOR = generate_key(5, minor_mode)
Gb_MINOR = generate_key(6, minor_mode)
G_MINOR = generate_key(7, minor_mode)
Ab_MINOR = generate_key(8, minor_mode)
A_MINOR = generate_key(9, minor_mode)
Bb_MINOR = generate_key(10, minor_mode)
B_MINOR = generate_key(11, minor_mode)

if __name__ == '__main__':
    assert(np.array_equal(major_mode(72), np.array([72, 74, 76, 77, 79, 81, 83])))
    assert(np.array_equal(minor_mode(72), np.array([72, 74, 75, 77, 79, 80, 82])))

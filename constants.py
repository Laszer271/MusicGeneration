import numpy as np

PROLONGATION = -2
REST = -1
LOWEST_PITCH = 0 # has to be C for proper key defining
HIGHEST_PITCH = 127
OCTAVE_LENGTH = 12
FULL_OCTAVES_NO = int(np.floor(HIGHEST_PITCH / OCTAVE_LENGTH))

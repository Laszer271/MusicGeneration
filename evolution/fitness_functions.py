import numpy as np
from . import features
from .utils import tonality

def statistical_fitness_function(gen_vec, music_key):
    result = 0
    for feature in features.statistical_features:
        result = result + feature[1] * np.exp( (-np.power(( feature[0](gen_vec, music_key) - feature[2] ), 2)) / (2 * np.power(feature[3], 2) ) )
    return result

if __name__ == "__main__":
    test_vector = np.array([60, -2, -2, -2, 62, -2, -2, -2, 64, -2, -2, -2, 65, -2, -2, -2,
                            67, -2, -2, -2, 69, -2, -2, -2, 71, -2, -2, -2, 72, -2, -2, -2,
                            -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2,
                            72, -2, -2, -2, 71, -2, -2, -2, 69, -2, -2, -2, 67, -2, -2, -2,
                            65, -2, -2, -2, 64, -2, -2, -2, 62, -2, -2, -2, 60, -2, -2, -2])
    print(statistical_fitness_function(test_vector, tonality.C_MAJOR))
from evolution.evolution import Evolution
from evolution.reproduction import one_point_crossover
from evolution.population_generation import generate_music_vectors
from evolution.selection import roulette_selection
from evolution.fitness_functions import statistical_fitness_function
from evolution import mutations
from evolution.utils import utils
from evolution.utils import tonality
import numpy as np

mutations_functions = (mutations.single_note_transposition,
                       mutations.interval_mutation,
                       mutations.note_position_mutation,
                       mutations.rest_to_note_mutation,
                       mutations.note_to_rest_mutation,
                       mutations.note_to_prolongation_mutation,
                       mutations.prolongation_to_note_mutation,
                       mutations.long_to_short_ratio_mutation)
reproduction_function = one_point_crossover
fitness_function = statistical_fitness_function
selection_function = roulette_selection
population_generation_function = generate_music_vectors

POPULATION_SIZE = 10
PROBS = utils.PROBS
SONG_SIZE = 64
population_kwargs = {'song_size': SONG_SIZE,
                     'population_size': POPULATION_SIZE,
                     'probabilities': PROBS}

evolution_model = Evolution(mutations_functions,
                            reproduction_function,
                            fitness_function,
                            selection_function,
                            population_generation_function,
                            tonality=tonality.F_MAJOR)

evolution_model.initialize_population(population_kwargs)
evolution_model.start(n_epochs=10000)
songs = evolution_model.get_population(n_best=10)
songs = np.array(songs)

np.save('generated_songs.npy', songs)

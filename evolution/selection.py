import numpy as np

def roulette_selection(population, scores, size_to_select):
    #print(population)
    population, idx = np.unique(population, axis=0, return_index=True)
    scores = np.array(scores)[idx]
    new_population_indices = [np.argmax(scores)] # elite strategy
    temp_population = population[1:]
    temp_scores = scores[1:]
    pop_length = len(temp_population)
    
    probs = temp_scores / np.sum(temp_scores)
    new_population_indices.extend(np.random.choice(range(pop_length),
                                           size=min(size_to_select-1, pop_length),
                                           p=probs,
                                           replace=False))
    return list(population[new_population_indices])
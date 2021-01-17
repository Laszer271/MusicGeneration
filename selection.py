import numpy as np

def roulette_selection(population, scores, size_to_select):
    #print(population)
    population, idx = np.unique(population, axis=0, return_index=True)
    scores = np.array(scores)[idx]
    new_population_indices = [np.argmax(scores)] # elite strategy
    
    probs = scores / np.sum(scores)
    new_population_indices.extend(np.random.choice(range(len(population)),
                                           size=min(size_to_select-1, len(population)),
                                           p=probs,
                                           replace=False))
    return list(population[new_population_indices])
import numpy as np

def one_point_crossover(population, n_children=None):
    if n_children is None:
        n_children = len(population) // 2
    
    length = len(population[0])
    point_threshold_pos = length - 1
    children = []
    for i in range(n_children):
        parents = np.random.randint(0, length, 2)
        parent1 = population[parents[0]]
        parent2 = population[parents[1]]
        
        cross_point = np.random.randint(1, point_threshold_pos)
        child = parent1.copy()
        child[cross_point:] = parent2[cross_point:]
        children.append(child)
        
    return np.array(children)
import numpy as np

class Evolution():
    
    def __init__(self, mutations, reproduction_function, fitness_function, 
                 selection_function, population_generation, mutations_probs=0.1):
        self.mutations = mutations
        self.reproduction_function = reproduction_function
        self.fitness_function = fitness_function
        self.selection_function = selection_function
        self.population_generation = population_generation
        try: 
            iter(mutations_probs)
            self.mutations_probs = mutations_probs
        except:
            self.mutations_probs = [mutations_probs for _ in mutations]
        
    def initialize_population(self, population_size, scale, prolongation_prob, rest_prob):
        self.change_population_size(population_size)
        kwargs = {'population_size': population_size,
                  'scale': scale,
                  'prolongation_prob': prolongation_prob,
                  'rest_prob': rest_prob}
        self.population = self.population_generation(**kwargs)
        
    def change_population_size(self, population_size):
        self.populaton_size = population_size
        
    def score_all(self, population):
        return np.array([self.fitness_function(x) for x in population])
    
    def get_population(self, n_best=None, return_scores=False):
        scores = self.score_all(self.population)
        idx = scores.argsort()[::-1]
        population = np.array(self.population)[idx]
        if n_best is not None:
            population = population[:n_best]
            
        if not return_scores:
            return population
        else:
            scores = scores[idx]
            return population, scores[:len(population)]
        
    def start(self, n_epochs):
        for epoch in range(n_epochs):
            parents_scores = self.score_all(self.population)
            children_population = self.reproduction_function(self.population,
                                                             parents_scores)
            new_children = []
            for child in children_population:
                for mutation, prob in zip(self.mutations, self.mutations_probs):
                    if np.random.random() <= prob:
                        child = mutation(child)
                new_children.append(child)
            children_scores = self.score_all(new_children)
            
            new_population = self.population + new_children
            scores = parents_scores + children_scores
            self.population = self.selection_function(new_population, scores, self.populaton_size)
            
            
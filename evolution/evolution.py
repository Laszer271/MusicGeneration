import numpy as np
from .utils import tonality

class Evolution():
    
    def __init__(self, mutations, reproduction_function, fitness_function, 
                 selection_function, population_generation, mutations_probs=0.1,
                 tonality=tonality.C_MAJOR):
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
        self.tonality = tonality
        
    def initialize_population(self, kwargs):
        self.change_population_size(kwargs['population_size'])
        self.population = self.population_generation(**kwargs)
        
    def change_population_size(self, population_size):
        self.populaton_size = population_size
        
    def score_all(self, population):
        return [self.fitness_function(x, self.tonality) for x in population]
    
    def get_population(self, n_best=None, return_scores=False):
        population = np.unique(self.population, axis=0)
        scores = np.array(self.score_all(population))
        idx = scores.argsort()[::-1]
        population = np.array(population)[idx]
        if n_best is not None:
            population = population[:n_best]
            
        if not return_scores:
            return population
        else:
            scores = scores[idx]
            return population, scores[:len(population)]
        
    def start(self, n_epochs, mutate_parents=True, mutate_children=True, can_parents_prevail=True):
        for epoch in range(n_epochs):
            parents_scores = self.score_all(self.population)
            print(f'Epoch: {epoch}, Max score: {np.max(parents_scores)}, Mean score: {np.mean(parents_scores)}')
            children_population = self.reproduction_function(self.population)
            population_to_mutate = []
            if mutate_parents:
                population_to_mutate.extend(self.population)
            if mutate_children:
                population_to_mutate.extend(children_population)
                
            mutated_population = []
            for x in population_to_mutate:
                mutated_x = x.copy()
                for mutation, prob in zip(self.mutations, self.mutations_probs):
                    if np.random.random() <= prob:
                        mutated_x = mutation(mutated_x)
                mutated_population.append(mutated_x)
            mutated_scores = self.score_all(mutated_population)
            
            if can_parents_prevail:
                new_population = self.population + mutated_population
                scores = parents_scores + mutated_scores
            else: 
                new_population = mutated_population
                scores = mutated_scores

            self.population = self.selection_function(new_population, scores, self.populaton_size)
            
            
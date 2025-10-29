"""
Genetic Algorithm - Evolve forms through natural selection.
"""

import numpy as np
from typing import List, Dict, Callable, Tuple


class GeneticFormOptimizer:
    """Evolve architectural forms using genetic algorithms."""
    
    def __init__(self,
                 population_size: int = 50,
                 mutation_rate: float = 0.1,
                 crossover_rate: float = 0.7):
        """
        Initialize genetic optimizer.
        
        Args:
            population_size: Number of individuals in population
            mutation_rate: Probability of mutation
            crossover_rate: Probability of crossover
        """
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generation = 0
    
    def initialize_population(self,
                            genome_length: int,
                            gene_range: Tuple[float, float] = (0, 1)) -> List[np.ndarray]:
        """
        Create initial random population.
        
        Args:
            genome_length: Length of genome (number of parameters)
            gene_range: Range of gene values (min, max)
            
        Returns:
            List of genomes
        """
        min_val, max_val = gene_range
        population = []
        
        for _ in range(self.population_size):
            genome = np.random.uniform(min_val, max_val, genome_length)
            population.append(genome)
        
        return population
    
    def evaluate_fitness(self,
                        population: List[np.ndarray],
                        fitness_func: Callable) -> List[float]:
        """
        Evaluate fitness of all individuals.
        
        Args:
            population: List of genomes
            fitness_func: Function that takes genome and returns fitness score
            
        Returns:
            List of fitness scores
        """
        return [fitness_func(genome) for genome in population]
    
    def selection_tournament(self,
                            population: List[np.ndarray],
                            fitness_scores: List[float],
                            tournament_size: int = 3) -> np.ndarray:
        """
        Select individual using tournament selection.
        
        Args:
            population: List of genomes
            fitness_scores: List of fitness scores
            tournament_size: Number of individuals in tournament
            
        Returns:
            Selected genome
        """
        # Randomly select tournament_size individuals
        indices = np.random.choice(len(population), tournament_size, replace=False)
        
        # Find best individual in tournament
        best_idx = indices[np.argmax([fitness_scores[i] for i in indices])]
        
        return population[best_idx].copy()
    
    def crossover_single_point(self,
                              parent1: np.ndarray,
                              parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform single-point crossover.
        
        Args:
            parent1: First parent genome
            parent2: Second parent genome
            
        Returns:
            Tuple of two offspring genomes
        """
        if np.random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        # Select crossover point
        point = np.random.randint(1, len(parent1))
        
        # Create offspring
        offspring1 = np.concatenate([parent1[:point], parent2[point:]])
        offspring2 = np.concatenate([parent2[:point], parent1[point:]])
        
        return offspring1, offspring2
    
    def crossover_uniform(self,
                         parent1: np.ndarray,
                         parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform uniform crossover.
        
        Args:
            parent1: First parent genome
            parent2: Second parent genome
            
        Returns:
            Tuple of two offspring genomes
        """
        if np.random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        # Create mask
        mask = np.random.random(len(parent1)) < 0.5
        
        # Create offspring
        offspring1 = np.where(mask, parent1, parent2)
        offspring2 = np.where(mask, parent2, parent1)
        
        return offspring1, offspring2
    
    def mutation_gaussian(self,
                         genome: np.ndarray,
                         mutation_strength: float = 0.1) -> np.ndarray:
        """
        Apply Gaussian mutation.
        
        Args:
            genome: Genome to mutate
            mutation_strength: Standard deviation of mutation
            
        Returns:
            Mutated genome
        """
        mutated = genome.copy()
        
        # Create mutation mask
        mutation_mask = np.random.random(len(genome)) < self.mutation_rate
        
        # Apply Gaussian noise to selected genes
        mutations = np.random.normal(0, mutation_strength, len(genome))
        mutated[mutation_mask] += mutations[mutation_mask]
        
        return mutated
    
    def evolve_generation(self,
                         population: List[np.ndarray],
                         fitness_scores: List[float],
                         elitism: int = 2) -> List[np.ndarray]:
        """
        Evolve one generation.
        
        Args:
            population: Current population
            fitness_scores: Fitness scores
            elitism: Number of best individuals to keep unchanged
            
        Returns:
            New population
        """
        new_population = []
        
        # Elitism: keep best individuals
        if elitism > 0:
            elite_indices = np.argsort(fitness_scores)[-elitism:]
            for idx in elite_indices:
                new_population.append(population[idx].copy())
        
        # Generate rest of population
        while len(new_population) < self.population_size:
            # Selection
            parent1 = self.selection_tournament(population, fitness_scores)
            parent2 = self.selection_tournament(population, fitness_scores)
            
            # Crossover
            offspring1, offspring2 = self.crossover_uniform(parent1, parent2)
            
            # Mutation
            offspring1 = self.mutation_gaussian(offspring1)
            offspring2 = self.mutation_gaussian(offspring2)
            
            new_population.append(offspring1)
            if len(new_population) < self.population_size:
                new_population.append(offspring2)
        
        self.generation += 1
        return new_population[:self.population_size]
    
    def optimize(self,
                genome_length: int,
                fitness_func: Callable,
                generations: int = 100,
                gene_range: Tuple[float, float] = (0, 1),
                verbose: bool = True) -> Dict:
        """
        Run complete optimization.
        
        Args:
            genome_length: Length of genome
            fitness_func: Fitness function
            generations: Number of generations to evolve
            gene_range: Range of gene values
            verbose: Print progress
            
        Returns:
            Dictionary with best genome and history
        """
        # Initialize
        population = self.initialize_population(genome_length, gene_range)
        best_fitness_history = []
        avg_fitness_history = []
        
        for gen in range(generations):
            # Evaluate
            fitness_scores = self.evaluate_fitness(population, fitness_func)
            
            # Track statistics
            best_fitness = max(fitness_scores)
            avg_fitness = np.mean(fitness_scores)
            best_fitness_history.append(best_fitness)
            avg_fitness_history.append(avg_fitness)
            
            if verbose and gen % 10 == 0:
                print(f"Generation {gen}: Best={best_fitness:.4f}, Avg={avg_fitness:.4f}")
            
            # Evolve
            if gen < generations - 1:
                population = self.evolve_generation(population, fitness_scores)
        
        # Get best individual
        final_fitness = self.evaluate_fitness(population, fitness_func)
        best_idx = np.argmax(final_fitness)
        best_genome = population[best_idx]
        
        return {
            'best_genome': best_genome,
            'best_fitness': final_fitness[best_idx],
            'population': population,
            'fitness_scores': final_fitness,
            'best_fitness_history': best_fitness_history,
            'avg_fitness_history': avg_fitness_history,
            'generations': generations
        }

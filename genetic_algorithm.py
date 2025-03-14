import random
import numpy as np

class Individual:
    def __init__(self, chromosome_length):
        self.chromosome = self.initialize_chromosome(chromosome_length)
        self.fitness = 0

    def initialize_chromosome(self, length):
        return [random.randint(0, 1) for _ in range(length)]

    def calculate_fitness(self, target):
        self.fitness = sum(1 for a, b in zip(self.chromosome, target) if a == b)

class GeneticAlgorithm:
    def __init__(self, population_size, chromosome_length, mutation_rate, target):
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.mutation_rate = mutation_rate
        self.target = target
        self.population = self.initialize_population()

    def initialize_population(self):
        return [Individual(self.chromosome_length) for _ in range(self.population_size)]

    def evaluate_population(self):
        for individual in self.population:
            individual.calculate_fitness(self.target)

    def select_parents(self):
        total_fitness = sum(individual.fitness for individual in self.population)
        if total_fitness == 0:
            return random.choices(self.population, k=2)
        
        selection_probs = [individual.fitness / total_fitness for individual in self.population]
        return random.choices(self.population, weights=selection_probs, k=2)

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(0, self.chromosome_length - 1)
        child1_chromosome = parent1.chromosome[:crossover_point] + parent2.chromosome[crossover_point:]
        child2_chromosome = parent2.chromosome[:crossover_point] + parent1.chromosome[crossover_point:]
        return Individual(self.chromosome_length), Individual(self.chromosome_length)

    def mutate(self, individual):
        for i in range(len(individual.chromosome)):
            if random.random() < self.mutation_rate:
                individual.chromosome[i] = 1 - individual.chromosome[i]

    def run(self, generations):
        for generation in range(generations):
            self.evaluate_population()
            new_population = []
            for _ in range(self.population_size // 2):
                parent1, parent2 = self.select_parents()
                child1, child2 = self.crossover(parent1, parent2)
                self.mutate(child1)
                self.mutate(child2)
                new_population.extend([child1, child2])
            self.population = new_population
            
            best_fitness = max(individual.fitness for individual in self.population)
            print(f"Generation {generation}: Best Fitness = {best_fitness}")
            if best_fitness == self.chromosome_length:
                print("Optimal solution found!")
                break

if __name__ == "__main__":
    TARGET = [1, 0, 1, 1, 0, 1, 0, 1]
    POPULATION_SIZE = 20
    CHROMOSOME_LENGTH = len(TARGET)
    MUTATION_RATE = 0.01
    GENERATIONS = 100

    ga = GeneticAlgorithm(POPULATION_SIZE, CHROMOSOME_LENGTH, MUTATION_RATE, TARGET)
    ga.run(GENERATIONS)
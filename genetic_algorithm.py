import random as rnd
import json


def import_graph():
    """
    Import the graph from the JSON file.
    """
    with open('graph.json', 'r') as f:
        dic = json.load(f)

    # Convert the keys from string to integer
    return {int(key): value for key, value in dic.items()}

def generate_initial_solutions():
    """
    Generate initial solutions.
    """
    initial_solutions = []

    for _ in range(N):
        string = ''
        for _ in range(16):
            string += rnd.choice(colors)
        initial_solutions.append(string)

    return initial_solutions

def fitness_function(solutions):
    """
    Calculate the fitness of each solution and return a list of fitness values. Fitness value
    is the number of conflicts in the graph (number of edges between nodes with the same color).
    """
    fitness_list = []
    
    for solution in solutions:
        fitness = 0
        
        for i in range(1,17):
            node_color = solution[i-1]
            neighbors = graph_dict[i]
            
            for neighbor in neighbors:
                neighbor_color = solution[neighbor-1]
                if neighbor_color == node_color:
                    fitness += 1
                    
        fitness_list.append(fitness)
        
    fitness_list = [x//2 for x in fitness_list] # Each edge is counted twice, so divide the fitness value by 2.
    sum_fitness = sum(fitness_list)
    fitness_list = [1-x/sum_fitness for x in fitness_list] # Normalizing the fitness values and converting to maximization problem.
    return fitness_list

def partial_population_renewal():
    """
    Partial population renewal.
    """
    number_of_renewed_solutions = int(N*0.6) # Number of solutions that will be replaced by the new generation.
    if number_of_renewed_solutions % 2 != 0:
        number_of_renewed_solutions += 1
    
    return number_of_renewed_solutions

def tournament_selection(fitness_list, number_of_renewed_solutions):
    """
    Tournament selection.
    """
    tournament_size = 3
    mating_pool = []
    pair = []
    sum_fitness = int(sum(fitness_list))
    
    def select_a_competitor():
        """
        Select a competitor from the tournament using cumulative probability distribution.
        """
        rnd_num = rnd.uniform(0, cpd[-1]) # Random number between 0 and cpd[-1], where cpd[-1] is the highest value we can get.
        for i in range(len(cpd)):
            if rnd_num <= cpd[i]:
                selected_parent = competitors[cumulative_probality_distribution.index(cpd[i])]
                if selected_parent not in pair:
                    return selected_parent
                else:
                    cpd.pop(i)
                    return select_a_competitor()
                        
    for _ in range(number_of_renewed_solutions):
        competitors = rnd.sample(range(len(fitness_list)), tournament_size)
        fitnesses = [fitness_list[competitor] for competitor in competitors]
        relative_fitnesses = [fitness/sum_fitness for fitness in fitnesses]
        cumulative_probality_distribution = [sum(relative_fitnesses[:i+1]) for i in range(len(relative_fitnesses))]
        cpd = sorted(cumulative_probality_distribution)
        selected_parent = select_a_competitor()
        
        if len(pair) < 2:
            pair.append(selected_parent)
        
        if len(pair) == 2:
            while pair in mating_pool or pair[::-1] in mating_pool:
                pair = []
                pair.append(selected_parent)
                selected_parent = select_a_competitor()
                pair.append(selected_parent)
            mating_pool.append(pair)
            pair = []

    return mating_pool

def one_point_crossover(solutions, mating_pool):
    """
    One-point crossover.
    """
    new_solutions = []
    for pair in mating_pool:
        crossover_point = rnd.randint(1, 15)
        new_solutions.append(solutions[pair[0]][:crossover_point] + solutions[pair[1]][crossover_point:])
        new_solutions.append(solutions[pair[1]][:crossover_point] + solutions[pair[0]][crossover_point:])
    return new_solutions

def mutation(solutions, fitness_list):
    """
    Mutation is applied to the solutions with the lowest fitness values.
    """
    number_of_mutations = int(N*0.1) # Number of solutions that will be mutated.
    fl = fitness_list.copy()
    mutated_solutions = []
    mutated_solutions_indexes = []
    
    while number_of_mutations > 0:
        min_fitness_idx = fl.index(min(fl))
        fl.pop(min_fitness_idx)
        solution = solutions[min_fitness_idx]
        rnd_idx = rnd.randint(0, 15)
        rnd_color = rnd.choice(colors)
        solution = solution[:rnd_idx] + rnd_color + solution[rnd_idx+1:]
        mutated_solutions.append(solution)
        mutated_solutions_indexes.append(min_fitness_idx)
        number_of_mutations -= 1
        
    return mutated_solutions, mutated_solutions_indexes

def elitism(solutions, fitness_list):
    """
    Find the solution with the highest fitness value and return it as the elite solution.
    """
    elite_solution = solutions[fitness_list.index(max(fitness_list))]
    elite_solution_index = fitness_list.index(max(fitness_list))

def choose_the_remaining_solutions(solutions, crossover_len, mutated_solutions_indexes, elite_solution_index):
    """
    Choose the remaining solutions from the initial solutions. This implementation
    is choosing the solutions that are not selected for mutation or elitism.
    """
    remaining_solutions_indexes = []
    mutation_len = len(mutated_solutions_indexes)
    size_of_remaining_solutions = N - crossover_len - mutation_len - 1 # -1 for the elite solution.
    
    while size_of_remaining_solutions > 0:
        rnd_idx = rnd.randint(0, N-1)
        while rnd_idx in mutated_solutions_indexes or rnd_idx == elite_solution_index or rnd_idx in remaining_solutions_indexes:
            rnd_idx = rnd.randint(0, N-1)
        remaining_solutions_indexes.append(rnd_idx)
        size_of_remaining_solutions -= 1
        
    return [solutions[idx] for idx in remaining_solutions_indexes]


if __name__ == '__main__':
    colors = ['B', 'R', 'G', 'Y'] # Blue, Red, Green, Yellow
    N = 6 # Number of initial solutions
    graph_dict = import_graph()
    initial_solutions = generate_initial_solutions()
    number_of_renewed_solutions = partial_population_renewal()
    
    fitness_list = fitness_function(initial_solutions)
    mating_pool = tournament_selection(fitness_list, number_of_renewed_solutions)
    print(f'Number of renewed solutions: {number_of_renewed_solutions}')
    crossovered_solutions = one_point_crossover(initial_solutions, mating_pool)
    mutated_solutions, mutated_solutions_indexes = mutation(initial_solutions, fitness_list)
    elite_solution, elite_solution_index = elitism(initial_solutions, fitness_list)
    remaining_solutions = choose_the_remaining_solutions(initial_solutions, len(crossovered_solutions), mutated_solutions_indexes, elite_solution_index)
    
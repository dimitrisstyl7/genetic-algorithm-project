import random as rnd
import json
import time
import networkx as nx
import matplotlib.pyplot as plt

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
        solution = ''
        for _ in range(16):
            solution += rnd.choice(colors)
        initial_solutions.append(solution)

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
    return elite_solution, elite_solution_index

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

def generate_new_population(crossovered_solutions, mutated_solutions, elite_solution, remaining_solutions):
    """
    Generate the new population.
    """
    new_population = []
    for solution in crossovered_solutions:
        new_population.append(solution)
    for solution in mutated_solutions:
        new_population.append(solution)
    for solution in remaining_solutions:
        new_population.append(solution)
    new_population.append(elite_solution)
    
    return new_population

def visualize_the_solution(solution):
    """
    Visualize the solution.
    """
    # Initialize an empty graph
    G = nx.Graph()

    # Add nodes to the graph
    G.add_nodes_from(graph_dict.keys())

    # Add edges to the graph
    for node, neighbors in graph_dict.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Define the colors of the nodes
    node_colors = []
    for i in range(len(solution)):
        if solution[i] == 'B':
            node_colors.append('blue')
        elif solution[i] == 'R':
            node_colors.append('red')
        elif solution[i] == 'G':
            node_colors.append('green')
        elif solution[i] == 'Y':
            node_colors.append('yellow')

    # Define the layout of the nodes
    pos = nx.shell_layout(G)

    # Set the figure size
    plt.figure(figsize=(8, 6))

    # Draw the graph
    nx.draw(G,  pos=pos, with_labels=True, node_color=node_colors, edge_color='black', node_size=1000, font_size=12, font_weight='bold')

    # Show the plot
    plt.show()

def solve_graph_coloring_problem():
    """
    Solve the graph coloring problem using genetic algorithm. If solution is not found
    in the given time limit, the algorithm stops and prints the best solution found.
    """
    solutions = generate_initial_solutions()
    best_solution = None
    best_solution_fitness = 0.0
    time_limit = 1 # Time limit in seconds.
    start_time = time.time()
    
    while time.time() - start_time < time_limit: # If the time limit is exceeded, the algorithm stops.
        number_of_renewed_solutions = partial_population_renewal()
        fitness_list = fitness_function(solutions)
        
        if max(fitness_list) == 1.0: # If a solution is found, visualize it and stop the algorithm.
            best_solution = solutions[fitness_list.index(max(fitness_list))]
            print('Solution found!')
            visualize_the_solution(best_solution)
            return
        
        mating_pool = tournament_selection(fitness_list, number_of_renewed_solutions)
        crossovered_solutions = one_point_crossover(solutions, mating_pool)
        mutated_solutions, mutated_solutions_indexes = mutation(solutions, fitness_list)
        elite_solution, elite_solution_index = elitism(solutions, fitness_list)
        remaining_solutions = choose_the_remaining_solutions(solutions, len(crossovered_solutions), mutated_solutions_indexes, elite_solution_index)
        solutions = generate_new_population(crossovered_solutions, mutated_solutions, elite_solution, remaining_solutions)
        
        if max(fitness_list) > best_solution_fitness:
            best_solution = solutions[fitness_list.index(max(fitness_list))]
            best_solution_fitness = max(fitness_list)
    
    print('Solution not found, best solution found is:')
    visualize_the_solution(best_solution) # If solution is not found, visualize the best solution found.


if __name__ == '__main__':
    colors = ['B', 'R', 'G', 'Y'] # Blue, Red, Green, Yellow
    N = 100 # Number of initial solutions
    graph_dict = import_graph()
    solve_graph_coloring_problem()
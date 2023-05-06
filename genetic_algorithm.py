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

    # Generate N random solutions
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
    number_of_renewed_solutions = int(N*0.3) # Number of solutions that will be replaced by the new generation.
    if number_of_renewed_solutions % 2 != 0:
        number_of_renewed_solutions += 1
    
    directly_passed_solutions = N - number_of_renewed_solutions # Number of solutions that will be directly passed to the next generation.
    return number_of_renewed_solutions, directly_passed_solutions

def tournament_selection(fitness_list, number_of_renewed_solutions):
    """
    Tournament selection.
    """
    tournament_size = 3
    mating_pool = []
    pair = []
    sum_fitness = sum(fitness_list)
    
    def select_a_competitor():
        """
        Select a competitor from the tournament using cumulative probability distribution.
        """
        rnd_num = rnd.random() # Random number between 0 and 1
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
        if len(pair) == 2:
            mating_pool.append(pair)
            pair = []
        else:
            pair.append(selected_parent)
            
    return mating_pool

if __name__ == '__main__':
    colors = ['B', 'R', 'G', 'Y'] # Blue, Red, Green, Yellow
    N = 5 # Number of initial solutions
    graph_dict = import_graph()
    initial_solutions = generate_initial_solutions()
    fitness_list = fitness_function(initial_solutions)
    number_of_renewed_solutions, directly_passed_solutions = partial_population_renewal()
    print(f'Number of renewed solutions: {number_of_renewed_solutions}')
    mating_pool = tournament_selection(fitness_list, number_of_renewed_solutions)
    #print(mating_pool)
    

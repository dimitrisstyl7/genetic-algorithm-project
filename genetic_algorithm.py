import random
import json
import copy

def generate_initial_solutions():
    """
    Generate initial solutions.
    """
    initial_solutions = []

    # Generate N random solutions
    for _ in range(N):
        string = ''
        for _ in range(16):
            string += random.choice(colors)
        initial_solutions.append(string)

    return initial_solutions

def fitness_function(solutions):
    """
    Calculate the fitness of each solution and return a list of fitness values.
    """
    fitness = 0
    fitness_list = []
    
    for solution in solutions:
        dic = copy.deepcopy(graph_dict)
        print(graph_dict)
        for i in range(1,17):
            node_color = solution[i-1]
            neighbors = dic[i]
            for neighbor in neighbors:
                neighbor_color = solution[neighbor-1]
                if neighbor_color == node_color:
                    #print(f'Solution: {solutions.index(solution)+1}')
                    #print(f'Node {i} color: {node_color}, Neighbor {neighbor} color: {neighbor_color}')
                    fitness += 1
                    dic[neighbor].remove(i)
        fitness_list.append(fitness)
        fitness = 0
    return fitness_list

def import_graph():
    """
    Import the graph from the JSON file.
    """
    with open('graph.json', 'r') as f:
        dic = json.load(f)

    # Convert the keys from string to integer
    return {int(key): value for key, value in dic.items()}


if __name__ == '__main__':
    colors = ['B', 'R', 'G', 'Y'] # Blue, Red, Green, Yellow
    N = 2 # Number of initial solutions
    graph_dict = import_graph()
    initial_solutions = generate_initial_solutions()
    fitness_list = fitness_function(initial_solutions)
    
    #print(initial_solutions)
    print(fitness_list)
    
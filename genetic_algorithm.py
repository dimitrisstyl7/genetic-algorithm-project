import random
import json

colors = ['B', 'R', 'G', 'Y'] # Blue, Red, Green, Yellow
N = 100 # Number of initial solutions

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
    Calculate the fitness of each solution.
    """
    fitness = 0
    fitness_list = []
    
    for node, neighbors in graph_dict.items():
        pass
        

def import_graph():
    """
    Import the graph from the JSON file.
    """
    with open('graph.json', 'r') as f:
        dic = json.load(f)

    # Convert the keys from string to integer
    return {int(key): value for key, value in dic.items()}


if __name__ == '__main__':
    global graph_dict
    initial_solutions = generate_initial_solutions()
    graph_dict = import_graph()
    
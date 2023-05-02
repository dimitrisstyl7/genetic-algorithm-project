import json
import random 
import networkx as nx
import matplotlib.pyplot as plt

# Read the JSON file
with open('graph.json', 'r') as f:
    dic = json.load(f)

# Convert the keys from string to integer
graph_dict = {int(key): value for key, value in dic.items()}

# Initialize an empty graph
G = nx.Graph()

# Add nodes to the graph
G.add_nodes_from(graph_dict.keys())

# Add edges to the graph
for node, neighbors in graph_dict.items():
    for neighbor in neighbors:
        G.add_edge(node, neighbor)

# Generate random colors for the nodes
node_colors = [f'#{random.randrange(256**3):06x}' for _ in G.nodes()]

# Define the layout of the nodes
pos = nx.shell_layout(G)

# Set the figure size
plt.figure(figsize=(8, 6))

# Draw the graph
nx.draw(G, pos=pos, with_labels=True, node_color=node_colors, node_size=1000, font_size=12, font_weight='bold', edge_color='gray')

# Show the plot
plt.show()

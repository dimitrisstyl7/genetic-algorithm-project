# Graph Coloring with Genetic Algorithms

## [University of Piraeus](https://www.unipi.gr/en/home/) | [Department of Informatics](https://cs.unipi.gr/en/)
**Course**: Artificial Intelligence and Expert Systems

**Semester**: 6

**Project Completion Year**: 2023

## Description
This project implements a graph coloring algorithm using genetic algorithms.

The goal is to color a given graph using a limited palette of four colors: blue, red, green, and yellow, ensuring that no two adjacent vertices share the same color.

## Features
- **Random Initial Population**: The algorithm starts with a randomly generated population of potential solutions, consisting of 100 individuals represented as strings of length 16, where each character corresponds to a color (Blue, Green, Yellow, Red).
- **Fitness Function**: A custom fitness function evaluates the quality of each solution based on the number of conflicts (adjacent vertices with the same color). The fitness values are normalized to convert the minimization problem into a maximization problem.
- **Selection Process**: A tournament selection mechanism is employed to choose parent solutions for reproduction, with a partial population renewal rate of 60%.
- **Crossover and Mutation**: The algorithm incorporates single-point crossover and mutation techniques, where a character mutation is applied to 10% of the population with the lowest fitness values.
- **Elitism**: The best solution (with the highest fitness value) is carried over to the next generation to ensure that the quality of solutions does not degrade.
- **Population Maintenance**: The remaining solutions are randomly filled to maintain a population size of 100 for the next generation.
- **Graph Representation**: The input graph is represented in a JSON format, detailing nodes and their neighboring nodes, which is loaded at the start of the algorithm.
- **Visualization**: The final solution can be visualized through a graph representation, allowing for an intuitive understanding of the coloring results.

## How to Run
1. **Clone the repository**:
```bash
git clone https://github.com/dimitrisstyl7/genetic-algorithm-project-2023.git
```
2. **Navigate to the project directory**:
```bash
cd genetic-algorithm-project-2023
```
3. **Create and activate a virtual environment**:

_On Linux/Mac_
```bash
python3 -m venv venv
source venv/bin/activate
```

_On Windows_
```bash
python -m venv venv
venv\Scripts\activate
```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```
5. **Run the program**:

_On Linux/Mac_
```bash
python3 genetic_algorithm.py
```
_On Windows_
```bash
python genetic_algorithm.py
```

## Acknowledgments
This project was developed as part of the Artificial Intelligence and Expert Systems course at the University of Piraeus. Contributions and feedback are always welcome!

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

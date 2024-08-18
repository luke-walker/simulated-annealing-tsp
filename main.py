"""
    Luke Walker
    github.com/luke-walker
    Traveling Salesman Problem w/ Simulated Annealing Optimization
"""

from argparse import ArgumentParser
import csv
import os.path
from typing import Tuple

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

def calculate_distance(point1: np.ndarray, point2: np.ndarray) -> float:
    """Returns the Euclidean distance of two points"""
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5

def get_random_state(data: np.ndarray) -> np.ndarray:
    """Returns a random state consisting of the provided data points"""
    state = np.copy(data)
    np.random.shuffle(state)
    return state

def get_random_successor(current_state: np.ndarray) -> np.ndarray:
    """Returns a random successor to the current state"""
    n = len(current_state)
    index1, index2 = np.random.randint(0, n-1), np.random.randint(0, n-1)
    start, end = min(index1, index2), max(index1, index2)

    successor_state = np.copy(current_state)
    successor_state[start:end] = successor_state[start:end][::-1]

    return successor_state

def objective_function(state: np.ndarray) -> float:
    """Returns the total distance between all data points in the state"""
    n = len(state)
    obj_value = 0

    for i in range(n-1):
        obj_value += calculate_distance(state[i], state[i+1])
    obj_value += calculate_distance(state[n-1], state[0])

    return obj_value

def simulated_annealing(current_state: np.ndarray, temperature: float) -> Tuple[np.ndarray, float]:
    """Returns the next state and the current state's objective value"""
    current_obj_value = objective_function(current_state)
    next_state = get_random_successor(current_state)
    delta_cost = objective_function(next_state) - current_obj_value 

    if delta_cost < 0 or np.random.random() <= np.exp(-delta_cost / temperature):
        return next_state, current_obj_value
    
    return current_state, current_obj_value
    
if __name__ == "__main__":
    def exit_error(err: str) -> None:
        print(err)
        exit(1)

    # parse command-line arguments
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help=".csv file path (don't use with -n)", default=None)
    parser.add_argument("-n", "--count", type=int, help="# of random data points (don't use with -f)", default=None)
    parser.add_argument("-i", "--iterations", type=int, help="# of iterations to perform", default=None)
    parser.add_argument("-r", "--reheat", type=int, help="# of iterations before reheating", default=100)
    parser.add_argument("-s", "--seed", type=int, help="prng seed", default=None)
    args = parser.parse_args()

    # validate command-line arguments
    if args.file and args.count:
        exit_error("use either -f or -n, not both")
    if not args.file and not args.count:
        exit_error("either -f or -n must be specified")
    if args.file and not os.path.exists(args.file):
        exit_error(f"data file {args.data} does not exist")
    if args.count and args.count < 3:
        exit_error("data point count cannot be less than 3")
    if args.iterations and args.iterations < 1:
        exit_error("iteration count cannot be less than 1")
    if args.reheat < 1:
        exit_error("reheat count cannot be less than 1")

    if args.seed:
        np.random.seed(args.seed)
        
    # populate data points using either .csv file or random points
    points = []
    if args.file:
        with open(args.file, "r") as csv_file:
            for row in csv.DictReader(csv_file):
                points.append((float(row['x']), float(row['y'])))
    elif args.count:
        for _ in range(args.count):
            points.append((float(np.random.randint(1, 100)), float(np.random.randint(1, 100))))

    current_state = get_random_state(np.array(points, dtype=[('x', float), ('y', float)])) # initial state
    objective_values = []

    fig, (ax1, ax2) = plt.subplots(1, 2) # 1 = TSP, 2 = SA
    line1, = ax1.plot(current_state['x'], current_state['y'], linestyle="-", marker=".")
    line2, = ax2.plot([], [])

    ax2.set_xlabel("Iteration #")
    ax2.set_ylabel("Distance")

    def animate(i):
        global current_state

        temperature = 1 / ((i % args.reheat) + 1)
        current_state, objective_value = simulated_annealing(current_state, temperature)
        objective_values.append(objective_value)

        ax1.set_title(f"Current Distance: {objective_values[-1]:.2f}")
        ax2.set_title(f"Current Temperature: {temperature:.4f}")

        plot_data1 = np.concatenate((current_state, np.array(current_state[:1])))
        line1.set_data(plot_data1['x'], plot_data1['y'])
        line2.set_data([x for x in range(len(objective_values))], objective_values)

        ax2.relim()
        ax2.autoscale()

    anim_interval = 0.001
    if args.iterations:
        anim = animation.FuncAnimation(fig, animate, frames=args.iterations, interval=anim_interval, repeat=False)
    else:
        anim = animation.FuncAnimation(fig, animate, frames=args.reheat, interval=anim_interval, repeat=True)

    plt.show()
    print(f"final distance: {objective_values[-1]}")

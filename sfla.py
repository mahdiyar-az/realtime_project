import numpy as np

def objective_function(x):
    return np.sum(x**2)

def initialize_frogs(num_frogs, dim, lower_bound, upper_bound):
    return np.random.uniform(lower_bound, upper_bound, (num_frogs, dim))

def sort_frogs(frogs):
    return sorted(frogs, key=lambda x: objective_function(x))

def local_search(memeplex, best_global, lower_bound, upper_bound, max_iter=10):
    memeplex = memeplex.copy()
    for _ in range(max_iter):
        worst = memeplex[-1]
        best = memeplex[0]

        step = np.random.rand() * (best - worst)
        new_frog = worst + step
        new_frog = np.clip(new_frog, lower_bound, upper_bound)

        if objective_function(new_frog) < objective_function(worst):
            memeplex[-1] = new_frog
        else:
            step = np.random.rand() * (best_global - worst)
            new_frog = worst + step
            new_frog = np.clip(new_frog, lower_bound, upper_bound)
            if objective_function(new_frog) < objective_function(worst):
                memeplex[-1] = new_frog
            else:
                memeplex[-1] = np.random.uniform(lower_bound, upper_bound, worst.shape)

        memeplex = sort_frogs(memeplex)

    return memeplex

def sfla(num_frogs=20, num_memeplexes=5, dim=5, lower_bound=-10, upper_bound=10, num_iterations=50):
    frogs = initialize_frogs(num_frogs, dim, lower_bound, upper_bound)
    frogs = sort_frogs(frogs)

    for iteration in range(num_iterations):
        memeplexes = [[] for _ in range(num_memeplexes)]
        for i, frog in enumerate(frogs):
            memeplexes[i % num_memeplexes].append(frog)

        for i in range(num_memeplexes):
            memeplex = sort_frogs(memeplexes[i])
            best_global = frogs[0]
            memeplexes[i] = local_search(memeplex, best_global, lower_bound, upper_bound)

        frogs = [frog for memeplex in memeplexes for frog in memeplex]
        frogs = sort_frogs(frogs)

        print(f"Iteration {iteration + 1}, Best Fitness: {objective_function(frogs[0]):.4f}")

    return frogs[0], objective_function(frogs[0])

best_solution, best_fitness = sfla()
import copy
import numpy as np
import random

def evaluate_schedule(schedule, hard_tasks, soft_tasks, alpha=1.0, beta=1.0, gamma=10.0):
    total_qos = 0
    total_power = 0
    missed_deadlines = 0

    for task in schedule:
        exec_time = task["start"] + task["wcet"]
        if task["id"].startswith("H"):
            if exec_time > task["deadline"]:
                missed_deadlines += 1
        else:
            delay = max(0, exec_time - task["deadline"])
            qos = task["qos_weight"] * max(0, 1 - delay / task["deadline"])
            total_qos += qos

        total_power += task["wcet"] * 0.5
    fitness = alpha * total_qos - beta * total_power - gamma * missed_deadlines
    return fitness


def levy_flight(Lambda):
    sigma = (np.math.gamma(1 + Lambda) * np.sin(np.pi * Lambda / 2) /
             (np.math.gamma((1 + Lambda) / 2) * Lambda * 2**((Lambda - 1) / 2))) ** (1 / Lambda)
    u = np.random.normal(0, sigma)
    v = np.random.normal(0, 1)
    step = u / abs(v) ** (1 / Lambda)
    return step

def generate_initial_nests(tasks, n=10):
    nests = []
    for _ in range(n):
        shuffled = copy.deepcopy(tasks)
        random.shuffle(shuffled)
        time = 0
        for t in shuffled:
            t["start"] = time
            time += t["wcet"]
        nests.append(shuffled)
    return nests

def cuckoo_search(hard_tasks, soft_tasks, num_nests=15, max_iter=100, pa=0.25):
    all_tasks = hard_tasks + soft_tasks
    nests = generate_initial_nests(all_tasks, num_nests)
    fitness = [evaluate_schedule(n, hard_tasks, soft_tasks) for n in nests]
    best_idx = np.argmax(fitness)
    best_nest = nests[best_idx]

    for _ in range(max_iter):
        for i in range(num_nests):
            new_nest = copy.deepcopy(nests[i])
            step = int(levy_flight(1.5) * len(new_nest)) % len(new_nest)
            if step != 0:
                new_nest[step], new_nest[-1] = new_nest[-1], new_nest[step]

            time = 0
            for t in new_nest:
                t["start"] = time
                time += t["wcet"]

            new_fitness = evaluate_schedule(new_nest, hard_tasks, soft_tasks)
            if new_fitness > fitness[i]:
                nests[i] = new_nest
                fitness[i] = new_fitness

        for i in range(num_nests):
            if random.random() < pa:
                nests[i] = generate_initial_nests(all_tasks, 1)[0]
                fitness[i] = evaluate_schedule(nests[i], hard_tasks, soft_tasks)

        current_best_idx = np.argmax(fitness)
        if fitness[current_best_idx] > fitness[best_idx]:
            best_idx = current_best_idx
            best_nest = nests[best_idx]

    return best_nest, fitness[best_idx]

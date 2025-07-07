import random


def wfd_mapping(tasks, cores):
    tasks.sort(key=lambda t: -t.execution / t.period)
    for task in tasks:
        if (task.soft):
            continue
        min_core = min(cores, key=lambda c: sum(t.execution / t.period for t in c.tasks))
        min_core.add_task(task)
    return cores


def sfla(tasks, num_cores, num_frogs=30, memeplexes=5, iterations=50):
    def create_frog(tasks, num_cores):
        return [random.randint(0, num_cores - 1) for _ in tasks]

    def evaluate_frog(frog, tasks, num_cores):
        core_utils = [0.0] * num_cores
        for i, core in enumerate(frog):
            core_utils[core] += tasks[i].utilization()
        return max(core_utils)

    def move_frog(worst, best):
        new_frog = worst[:]
        for i in range(len(worst)):
            if random.random() < 0.5:
                new_frog[i] = best[i]
        return new_frog
    frogs = [create_frog(tasks, num_cores) for _ in range(num_frogs)]
    for _ in range(iterations):
        frogs.sort(key=lambda f: evaluate_frog(f, tasks, num_cores))
        groups = [frogs[i::memeplexes] for i in range(memeplexes)]
        for group in groups:
            group.sort(key=lambda f: evaluate_frog(f, tasks, num_cores))
            best = group[0]
            worst = group[-1]
            new_worst = move_frog(worst, best)
            if evaluate_frog(new_worst, tasks, num_cores) < evaluate_frog(worst, tasks, num_cores):
                group[-1] = new_worst
        frogs = [frog for group in groups for frog in group]
    best_frog = min(frogs, key=lambda f: evaluate_frog(f, tasks, num_cores))
    return best_frog

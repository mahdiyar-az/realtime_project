def wfd_mapping(tasks, cores):
    tasks.sort(key=lambda t: -t.execution / t.period)
    for task in tasks:
        if (task.soft):
            continue
        min_core = min(cores, key=lambda c: sum(t.execution / t.period for t in c.tasks))
        min_core.add_task(task)
    return cores




def wfd_mapping(tasks, cores):
    hard_tasks = [t for t in tasks if t.task_type == 'hard']
    hard_tasks.sort(key=lambda t: t.utilization, reverse=True)

    for task in hard_tasks:

        target_core = min(cores, key=lambda c: sum(t.utilization for t in c.tasks))
        target_core.tasks.append(task)

    return cores





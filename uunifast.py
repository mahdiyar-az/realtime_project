import random

from task import Task


def uunifast(num_tasks, total_utilization):
    utilizations = []
    sum_u = total_utilization
    for i in range(1, num_tasks):
        next_sum_u = sum_u * (random.random() ** (1 / (num_tasks - i)))
        utilizations.append(round(sum_u - next_sum_u , 3))
        sum_u = next_sum_u
    utilizations.append(round(sum_u,3))

    return utilizations

def generate_tasks(num_tasks,num_cores, core_efficiency):
    total_utilization = num_cores*core_efficiency
    utilizations = uunifast(num_tasks, total_utilization)
    print(utilizations)
    tasks = []
    for i, util in enumerate(utilizations):
        wcet = random.randint(10, 40)
        period = int(round((1/util) * wcet, 0))
        print(wcet,period)
        if period %2 == 1:
            period = period-1
        deadline = period

        if i % 5 < 3:
            task_type = 'hard'
        else:
            task_type = 'soft'

        task = Task(i + 1, util, wcet, period, deadline, task_type)
        tasks.append(task)

    return tasks

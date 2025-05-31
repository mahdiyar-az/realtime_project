import random
from time import sleep

from task import Task

def uunifast(n, u_total):
    utilizations = []
    sum_u = u_total
    for i in range(1, n):
        next_u = sum_u * random.uniform(0, 1) ** (1 / (n - i))
        utilizations.append(sum_u - next_u)
        sum_u = next_u
    utilizations.append(sum_u)
    return utilizations

def generate_tasks(n, m, u_total, soft=False):
    from task import Task
    import random

    tasks = []
    utilizations = uunifast(n, m*u_total)
    # print(utilizations)
    print(sum(utilizations))

    for u in utilizations:
        exec_time = random.randint(10, 400)

        raw_period = exec_time / u

        period = int(round(raw_period / 500.0)) * 500
        if period == 0:
            period = 500  # حداقل مقدار مجاز

        exec_time = int(u * period)
        if exec_time == 0:
            exec_time = 1

        task = Task(exec_time, period, period, soft)
        tasks.append(task)

    return tasks


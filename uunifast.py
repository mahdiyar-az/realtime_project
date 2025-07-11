import random
from time import sleep

from task import Task

def normalize_array(arr):
    b = arr.copy()  # کپی برای جلوگیری از تغییر آرایه اصلی
    b.sort()
    print(b)
    b[0]=(b[0]+b[len(b)-1])/3
    b[len(b)-1]=b[0]*2

    return b
def uunifast(n, u_total):

    utilizations = []
    sum_u = u_total
    for i in range(1, n):
        next_u = sum_u * random.uniform(0, 1) ** (1 / (n - i))
        utilizations.append(sum_u-next_u)
        sum_u = next_u
    utilizations.append(sum_u)
    while max(utilizations)>=1 :
        utilizations = normalize_array(utilizations)

    return utilizations

def generate_tasks(n, m, u_total):
    tasks = []
    utilizations = uunifast(n, m*u_total)
    for u in utilizations:
        exec_time = random.randint(10, 400)
        raw_period = exec_time / u
        period = int(round(raw_period / 500.0)) * 500
        if period == 0:
            period = 500

        exec_time = int(u * period)
        if exec_time == 0:
            exec_time = 1
        task = Task(len(tasks), exec_time, period, period, len(tasks)%5<2)
        tasks.append(task)
    return tasks


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
        # 1. exec_time تصادفی بین 10 و 400
        exec_time = random.randint(10, 400)

        # 2. محاسبه اولیه period
        raw_period = exec_time / u

        # 3. گرد کردن period به نزدیک‌ترین عدد بخش‌پذیر بر 200
        period = int(round(raw_period / 500.0)) * 500
        if period == 0:
            period = 500  # حداقل مقدار مجاز

        # 4. اصلاح exec_time با period جدید
        exec_time = int(u * period)
        if exec_time == 0:
            exec_time = 1  # حداقل اجرا برای جلوگیری از صفر شدن

        task = Task(exec_time, period, period, soft)
        tasks.append(task)

    return tasks


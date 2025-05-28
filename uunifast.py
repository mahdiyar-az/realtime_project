import random

from task import Task

def uunifast(num_tasks, total_utilization):
    utilizations = []
    sum_u = total_utilization

    for i in range(1, num_tasks):
        next_sum_u = sum_u * (random.random() ** (1 / (num_tasks - i)))
        ui = sum_u - next_sum_u

        # اگر مقدار بیشتر از 1 شد، آن را محدود کن
        if ui > 1:
            ui = 1
            next_sum_u = sum_u - ui

        utilizations.append(ui)
        sum_u = next_sum_u

    # آخرین مقدار را هم اضافه می‌کنیم
    last = sum_u
    if last > 1:
        last = 1
    utilizations.append(last)

    # نرمال‌سازی در صورت نیاز: اگر مجموع واقعی کمتر از مقدار خواسته‌شده شد
    total_current = sum(utilizations)
    if total_current < total_utilization:
        diff = total_utilization - total_current
        # تلاش برای توزیع اختلاف به عناصر کمتر از 1
        for i in range(len(utilizations)):
            gap = 1 - utilizations[i]
            add = min(gap, diff)
            utilizations[i] += add
            diff -= add
            if diff <= 0:
                break

    # نهایی: گرد کردن
    utilizations = [round(u, 3) for u in utilizations]
    return utilizations


def generate_tasks(num_tasks,num_cores, core_efficiency):
    total_utilization = num_cores*core_efficiency
    utilizations = uunifast(num_tasks, total_utilization)
    # print(utilizations)
    tasks = []
    for i, util in enumerate(utilizations):
        wcet = random.randint(10, 400)
        period = int(round((1/util) * wcet, 0))
        period = int(period / 500) * 500
        if period==0:
            period=500
        wcet =  int(round(util * period, 0))
        deadline = period
        arrival_time=0
        if i % 5 < 3:
            task_type = 'hard'
        else:
            arrival_time = random.randint(0, 400)
            task_type = 'soft'

        task = Task(i + 1, util, wcet, period, deadline, task_type,arrival_time)
        tasks.append(task)

    return tasks

import random
import numpy as np


def cuckoo(cores, tasks, num_nests=2, max_iter=4, pa=0.25):
    num_cores = len(cores)
    num_tasks = len(tasks)

    # تولید جمعیت اولیه (nests): تخصیص تصادفی تسک‌ها به هسته‌ها
    nests = [np.random.randint(0, num_cores, size=num_tasks) for _ in range(num_nests)]

    def fitness(assignments):
        loads = [0] * num_cores
        for task_index, core_index in enumerate(assignments):
            task = tasks[task_index]
            core = cores[core_index]
            start_time = find_earliest_slot(core, task.execution)
            if start_time is None:
                return float('inf')  # جواب نامعتبر
            loads[core_index] += task.duration
        return max(loads)  # هدف: کم کردن بیشترین بار روی یک هسته

    def levy_flight(Lambda):
        sigma = (np.math.gamma(1 + Lambda) * np.sin(np.pi * Lambda / 2) /
                 (np.math.gamma((1 + Lambda) / 2) * Lambda * 2 ** ((Lambda - 1) / 2))) ** (1 / Lambda)
        u = np.random.normal(0, sigma, size=num_tasks)
        v = np.random.normal(0, 1, size=num_tasks)
        step = u / (np.abs(v) ** (1 / Lambda))
        return step

    best_nest = None
    best_fit = float('inf')

    for iteration in range(max_iter):
        for i in range(num_nests):
            print(i,iteration,max_iter,num_nests)
            step = levy_flight(1.5)
            new_nest = nests[i] + step
            new_nest = np.clip(np.round(new_nest), 0, num_cores - 1).astype(int)

            f_new = fitness(new_nest)
            f_old = fitness(nests[i])
            if f_new < f_old:
                nests[i] = new_nest

            if f_new < best_fit:
                best_nest = new_nest.copy()
                best_fit = f_new

        # جایگزینی بخشی از بدترین لانه‌ها
        num_replace = int(pa * num_nests)
        worst_indices = sorted(range(num_nests), key=lambda i: fitness(nests[i]), reverse=True)
        for idx in worst_indices[:num_replace]:
            nests[idx] = np.random.randint(0, num_cores, size=num_tasks)

    # -----------------------------
    # تخصیص نهایی بهترین جواب به هسته‌ها
    # -----------------------------
    for i, core_index in enumerate(best_nest):
        task = tasks[i]
        core = cores[core_index]
        start_time = find_earliest_slot(core, task.duration)
        if start_time is not None:
            core.schedule.append({'start': start_time, 'end': task.execution+start_time, 'exec': task.execution, 'task': task})
            core.tasks.append(task)
        else:
            print(f"⚠️ Task {task.id} could not be scheduled on Core {core.id}")

    return best_nest  # فقط برای بررسی خروجی (اختیاری)


def find_earliest_slot(core, task_duration):
    occupied = []
    for a in core.schedule:
        # print(a)
        occupied.append((a["start"], a["exec"]))

    occupied.sort()

    current_time = 0
    while current_time + task_duration <= core.hyperperiod:
        conflict = False
        for s, e in occupied:
            if not (current_time + task_duration <= s or current_time >= e):
                conflict = True
                current_time = e
                break
        if not conflict:
            return current_time
    return None


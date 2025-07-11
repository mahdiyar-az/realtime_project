import random
import numpy as np


def cuckoo(cores, tasks, num_nests=5, max_iter=2, pa=0.25):
    num_cores = len(cores)
    num_tasks = len(tasks)
    nests = [np.random.randint(0, num_cores, size=num_tasks) for _ in range(num_nests)]

    def fitness(assignments):
        loads = [0] * num_cores
        for task_index, core_index in enumerate(assignments):
            task = tasks[task_index]
            core = cores[core_index]
            start_time = find_earliest_slot(core, task["execution"])
            if start_time is None:
                return float('inf')
            loads[core_index] += task["execution"]
        return max(loads)

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

        # جایگزینی لانه‌های ضعیف
        num_replace = int(pa * num_nests)
        worst_indices = sorted(range(num_nests), key=lambda i: fitness(nests[i]), reverse=True)
        for idx in worst_indices[:num_replace]:
            nests[idx] = np.random.randint(0, num_cores, size=num_tasks)

    # اجرای واقعی
    scheduled_tasks = []
    dropped_tasks = []

    if best_nest is None:
        return [], tasks  # همه دراپ میشن

    for i, core_index in enumerate(best_nest):
        task = tasks[i]
        core = cores[core_index]
        duration = task["execution"]

        start_time = find_earliest_slot(core, duration)

        if start_time is not None:
            core["schedule"].append({'start': start_time, 'end': start_time + duration, 'exec': duration, 'task': task})
            core["tasks"].append(task)
            scheduled_tasks.append({
                'task_id': task["id"],
                'core_id': core_index,
                'start': start_time,
                'end': start_time + duration,
                'parts': 1
            })
        else:
            # تلاش برای شکستن تسک
            success = False
            split_sizes = split_task(duration)
            temp_parts = []
            for part_size in split_sizes:
                assigned = False
                for c in cores:
                    part_start = find_earliest_slot(c, part_size)
                    if part_start is not None:
                        c["schedule"].append({'start': part_start, 'end': part_start + part_size, 'exec': part_size, 'task': task})
                        c["tasks"].append(task)
                        temp_parts.append({
                            'task_id': task["id"],
                            'core_id': c["id"],
                            'start': part_start,
                            'end': part_start + part_size,
                            'part_size': part_size
                        })
                        assigned = True
                        break
                if not assigned:
                    break
            if len(temp_parts) == len(split_sizes):
                scheduled_tasks.extend(temp_parts)
                success = True
            else:
                dropped_tasks.append(task["id"])

    return scheduled_tasks, dropped_tasks


def split_task(duration):
    # ساده‌ترین حالت تقسیم: تا جای ممکن به تکه‌های 3 و 2
    parts = []
    while duration > 0:
        if duration >= 3:
            parts.append(3)
            duration -= 3
        elif duration == 2:
            parts.append(2)
            duration -= 2
        else:
            parts.append(1)
            duration -= 1
    return parts



def find_earliest_slot(core, task_duration):
    # print(core,task_duration)
    occupied = []
    for a in core["schedule"]:
        # print(a)
        occupied.append((a["start"], a["exec"]))

    occupied.sort()

    current_time = 0
    d = core["hyperperiod"]*4
    if d==0:
        d=100000
    # print(core)
    while current_time + task_duration <= d:
        # print(current_time,task_duration,core["hyperperiod"])
        conflict = False
        for s, e in occupied:
            if not (current_time + task_duration <= s or current_time >= e):
                conflict = True
                current_time = e
                break
        if not conflict:
            return current_time
    return None


import random
import pandas as pd
import numpy as np

# -------- مرحله 1: تولید وظایف سخت --------
def generate_hard_tasks(n_tasks=20, wcet_range=(1, 5), period_range=(10, 100), seed=42):
    random.seed(seed)
    tasks = []
    for i in range(n_tasks):
        wcet = random.randint(*wcet_range)
        period = random.randint(*period_range)
        deadline = period  # در سیستم Real-Time سخت
        utilization = wcet / period
        tasks.append({
            "Task ID": f"H{i+1}",
            "Type": "Hard",
            "WCET": wcet,
            "Period": period,
            "Deadline": deadline,
            "Utilization": round(utilization, 4)
        })
    return tasks

# -------- مرحله 2: تولید وظایف نرم --------
def generate_soft_tasks(n_tasks=10, wcet_range=(1, 4), period_range=(20, 150), seed=24):
    random.seed(seed)
    tasks = []
    for i in range(n_tasks):
        wcet = random.randint(*wcet_range)
        period = random.randint(*period_range)
        deadline = period
        utilization = wcet / period
        tasks.append({
            "Task ID": f"S{i+1}",
            "Type": "Soft",
            "WCET": wcet,
            "Period": period,
            "Deadline": deadline,
            "Utilization": round(utilization, 4)
        })
    return tasks

# -------- مرحله 3: الگوریتم WFD برای زمان‌بندی وظایف سخت --------
def wfd_scheduler(tasks, n_cores):
    bins = [[] for _ in range(n_cores)]
    core_utils = [0.0] * n_cores

    # مرتب‌سازی وظایف بر اساس بهره‌وری نزولی
    tasks_sorted = sorted(tasks, key=lambda x: x['Utilization'], reverse=True)
    for task in tasks_sorted:
        # بدترین تناسب → بیشترین بهره‌وری باقی‌مانده
        idx = core_utils.index(min(core_utils))
        bins[idx].append(task)
        core_utils[idx] += task['Utilization']
    return bins, core_utils

# -------- مرحله 4: محاسبه Makespan --------
def calculate_makespan(task_bins):
    makespan = max(sum(task['WCET'] for task in bin) for bin in task_bins)
    return makespan

# -------- مرحله 5: توان مصرفی (مصرف فرضی: هر هسته با وظیفه > 0 مصرف دارد) --------
def calculate_power_usage(core_utils):
    return sum(1 for util in core_utils if util > 0)

# اجرای همه مراحل برای سیستم 8، 16، 32 هسته‌ای با بهره‌وری‌های مختلف
core_counts = [8, 16, 32]
util_levels = [0.25, 0.5, 0.75, 1.0]
results = []

# تولید وظایف
hard_tasks = generate_hard_tasks()
soft_tasks = generate_soft_tasks()
all_tasks = hard_tasks + soft_tasks

for cores in core_counts:
    for util_limit in util_levels:
        filtered_hard = [t for t in hard_tasks if t["Utilization"] <= util_limit]
        bins, core_utils = wfd_scheduler(filtered_hard, cores)
        makespan = calculate_makespan(bins)
        power = calculate_power_usage(core_utils)
        results.append({
            "Cores": cores,
            "Utilization Limit": util_limit,
            "Total Hard Tasks": len(filtered_hard),
            "Makespan": makespan,
            "Power Usage": power,
            "Max Core Util": round(max(core_utils), 3),
            "Avg Core Util": round(np.mean(core_utils), 3)
        })

results_df = pd.DataFrame(results)
results_df.head()

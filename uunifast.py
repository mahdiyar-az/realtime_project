import random
from time import sleep

from task import Task

def normalize_array(arr, max_val=0.99):
    arr = list(arr)  # کپی برای جلوگیری از تغییر آرایه اصلی
    total = sum(arr)

    # پیدا کردن اندیس عددهای بزرگ‌تر از ۱
    indices_above_1 = [i for i, x in enumerate(arr) if x > 1]

    # مقدار اضافه‌ای که باید جبران کنیم
    surplus = 0
    for i in indices_above_1:
        surplus += arr[i] - max_val
        arr[i] = max_val

    # حالا surplus رو بین عددهای کوچکتر از ۱ پخش می‌کنیم
    indices_below_1 = [i for i, x in enumerate(arr) if x < 1]

    total_below = sum(arr[i] for i in indices_below_1)

    for i in indices_below_1:
        if total_below == 0:
            break
        ratio = arr[i] / total_below
        arr[i] += surplus * ratio
        # اگر عدد از 1 بیشتر شد، دوباره محدودش کن (اختیاری)
        if arr[i] > 1:
            arr[i] = max_val

    # نرمال‌سازی نهایی برای حفظ مجموع
    scale = total / sum(arr)
    arr = [x * scale for x in arr]

    return arr
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
        task = Task(exec_time, period, period, len(tasks)%5<2)
        tasks.append(task)
    return tasks


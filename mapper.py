import heapq


def wfd_mapping(tasks, cores):
    hard_tasks = [t for t in tasks if t.task_type == 'hard']
    hard_tasks.sort(key=lambda t: t.utilization, reverse=True)

    for task in hard_tasks:
        print(task.utilization)
        print('---------------------------------')
        target_core = min(cores, key=lambda c: sum(t.utilization for t in c.tasks))
        target_core.tasks.append(task)

    return cores


def edf_schedule(core):
    jobs = core.jobs
    jobs.sort(key=lambda j: j.release_time)  # مرتب‌سازی بر اساس زمان release
    event_queue = jobs[:]  # صف jobهایی که هنوز release نشدن

    ready_queue = []  # heap بر اساس deadline
    schedule = []

    time = 0
    current_job = None
    next_release_index = 0

    while time < core.hyperperiod or current_job or ready_queue:
        # اضافه کردن jobهایی که now release شدن
        while next_release_index < len(jobs) and jobs[next_release_index].release_time <= time:
            job = jobs[next_release_index]
            heapq.heappush(ready_queue, (job.deadline, job))
            next_release_index += 1

        # preempt اگر job جدید با deadline زودتر وارد شد
        if current_job and ready_queue:
            next_deadline, peek_job = ready_queue[0]
            if peek_job.deadline < current_job.deadline:
                heapq.heappush(ready_queue, (current_job.deadline, current_job))
                current_job = None

        # اگر job فعلی نداریم، یکی از ready queue بردار
        if not current_job and ready_queue:
            _, current_job = heapq.heappop(ready_queue)

        if current_job:
            # تا زمانی که job تمام شود یا job جدیدی بیاید (release)
            next_event_time = min(
                jobs[next_release_index].release_time if next_release_index < len(jobs) else core.hyperperiod,
                time + current_job.remaining_time
            )

            duration = next_event_time - time
            schedule.append((time, current_job.task_id, duration))
            current_job.remaining_time -= duration
            time = next_event_time
            if current_job.remaining_time == 0:
                current_job.finished = True
                current_job = None
        else:
            # هیچ jobی نیست، بریم تا نزدیک‌ترین release
            if next_release_index < len(jobs):
                idle_until = jobs[next_release_index].release_time
                schedule.append((time, "IDLE", idle_until - time))
                time = idle_until
            else:
                break

    return schedule


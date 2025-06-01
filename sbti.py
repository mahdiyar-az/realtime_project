def sbti_schedule(soft_tasks, cores):
    for task in soft_tasks:
        scheduled = False
        for core in cores:
            for interval in core.get_slack_intervals():
                if task.execution <= interval[1] - interval[0]:
                    core.schedule_soft_task(task, interval)
                    scheduled = True
                    break
            if scheduled:
                break

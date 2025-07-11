class core:
    def __init__(self):
        self.tasks = []
        self.soft_tasks = []
        self.schedule = []
        self.hyperperiod = 0
        self.slack = []

    def add_task(self, task):
        self.tasks.append(task)
    def total_load(self):
        # print(len(self.schedule))
        return sum(t.execution for t, _ in self.schedule)
    def calculate_hyperperiod(self):
        from math import gcd
        from functools import reduce

        def lcm(a, b):
            return a * b // gcd(a, b)

        periods = [task.period for task in self.tasks]
        exec = [task.execution for task in self.tasks]
        # print(periods)
        self.hyperperiod = reduce(lcm, periods) if periods else 0

    def generate_jobs(self):
        self.jobs = []
        for task in self.tasks:
            for t in range(0, self.hyperperiod, task.period):
                # print(t,self.hyperperiod,task.period)
                # print(self.hyperperiod,task.period,t)
                self.jobs.append({
                    'release': t,
                    'deadline': t + task.deadline,
                    'execution': task.execution,
                    'task': task
                })

    def get_slack(self):
        current_time = 0

        for task2 in self.schedule:
            if current_time<task2["start"]:
                self.slack.append({
                    "start":current_time,
                    "end":task2["start"]
                })
                current_time=task2["end"]
            elif current_time<task2["end"]:
                current_time=task2["end"]
        if current_time < self.hyperperiod:
            self.slack.append({
                "start": current_time,
                "end": self.hyperperiod
            })
        return current_time
    def edf_schedule(self):
        time = 0
        self.schedule = []
        ready_jobs = []
        remaining = {}

        self.jobs = sorted(self.jobs, key=lambda j: j['release'])
        job_idx = 0
        current_job = None
        current_start = None

        while job_idx < len(self.jobs) or ready_jobs or current_job:
            # print(job_idx,len(self.jobs),ready_jobs,current_job)

            while job_idx < len(self.jobs) and self.jobs[job_idx]['release'] <= time:
                job = self.jobs[job_idx]
                ready_jobs.append(job)
                remaining[job['task']] = job['execution']
                job_idx += 1

            if ready_jobs:
                ready_jobs.sort(key=lambda j: j['deadline'])
                next_job = ready_jobs[0]
            else:
                next_job = None

            if current_job != next_job:
                if current_job is not None:
                    self.schedule.append({"start":current_start,"end": time,"exec":time-current_start})
                current_job = next_job
                current_start = time

            if current_job is None:
                if job_idx < len(self.jobs):
                    time = self.jobs[job_idx]['release']
                else:
                    break
            else:

                time_to_finish = remaining[current_job['task']]
                if job_idx < len(self.jobs):
                    time_to_next_release = self.jobs[job_idx]['release'] - time
                else:
                    time_to_next_release = float('inf')

                delta = min(time_to_finish, time_to_next_release)
                time += delta
                remaining[current_job['task']] -= delta

                if remaining[current_job['task']] == 0:
                    ready_jobs.remove(current_job)
                    self.schedule.append({"start":current_start,"end": time,"exec":time-current_start})

                    # self.schedule.append((current_start, time, current_job['task']))
                    current_job = None
                    current_start = None

    def get_earliest_start_time(self, task):
        self.get_slack()
        for task2 in self.slack:
            # print(task)
            if task.execution <= task2['end'] - task2["start"]:
                return task2["start"]


    def get_slack_intervals(self):
        slack = []
        if not self.schedule:
            slack.append((0, self.hyperperiod))
            return slack

        # self.schedule.sort()
        prev_end = 0
        #print(self.schedule[0])
        for item in self.schedule:
            # print(item["start"],prev_end)
            if item["start"] > prev_end:
                slack.append((prev_end, item["start"]))
            prev_end = max(prev_end, item["end"])
        if prev_end < self.hyperperiod:
            slack.append((prev_end, self.hyperperiod))
        return slack

    def schedule_soft_task(self, task, interval):
        start, end = interval
        self.soft_tasks.append(task)
        # self.schedule.append((start, start + task.execution, task))
        self.schedule.append({"start": start, "end": start + task.execution,"exec":task.execution})

        # self.schedule.sort()
        self.schedule = sorted(self.schedule,key =lambda x:x["start"])

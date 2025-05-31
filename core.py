class core:
    def __init__(self):
        self.tasks = []          # Hard tasks
        self.soft_tasks = []     # Soft tasks
        self.schedule = []       # (start_time, end_time, task)
        self.hyperperiod = 0

    def add_task(self, task):
        self.tasks.append(task)

    def calculate_hyperperiod(self):
        from math import gcd
        from functools import reduce

        def lcm(a, b):
            return a * b // gcd(a, b)

        periods = [task.period for task in self.tasks]
        exec = [task.execution for task in self.tasks]

        self.hyperperiod = reduce(lcm, periods) if periods else 0

    def generate_jobs(self):
        self.jobs = []
        for task in self.tasks:
            for t in range(0, self.hyperperiod, task.period):
                # print(self.hyperperiod,task.period,t)
                self.jobs.append({
                    'release': t,
                    'deadline': t + task.deadline,
                    'execution': task.execution,
                    'task': task
                })

    # def edf_schedule(self):
    #     time = 0
    #     sort_job = self.jobs.sort(key=lambda job: job['deadline'])
    #     for job in self.jobs:
    #         if time < job['release']:
    #             time = job['release']
    #         end = time + job['execution']
    #         self.schedule.append((time, end, job['task']))
    #         time = end

    def edf_schedule(self):
        time = 0
        self.schedule = []
        ready_jobs = []
        remaining = {}  # زمان باقی مانده برای هر job

        self.jobs = sorted(self.jobs, key=lambda j: j['release'])
        job_idx = 0
        current_job = None
        current_start = None

        while job_idx < len(self.jobs) or ready_jobs or current_job:
            # print(job_idx,len(self.jobs),ready_jobs,current_job)
            # اضافه کردن job هایی که release شدن
            while job_idx < len(self.jobs) and self.jobs[job_idx]['release'] <= time:
                job = self.jobs[job_idx]
                ready_jobs.append(job)
                remaining[job['task']] = job['execution']
                job_idx += 1

            # مرتب سازی بر اساس ددلاین
            if ready_jobs:
                ready_jobs.sort(key=lambda j: j['deadline'])
                next_job = ready_jobs[0]
            else:
                next_job = None

            if current_job != next_job:
                # اگر job فعلی عوض شد، رکورد قبلی رو ذخیره کن
                if current_job is not None:
                    self.schedule.append((current_start, time, current_job['task']))
                current_job = next_job
                current_start = time

            if current_job is None:
                # هیچ job آماده نیست، زمان رو می‌بریم جلو به زمان release بعدی
                if job_idx < len(self.jobs):
                    time = self.jobs[job_idx]['release']
                else:
                    break
            else:
                # پیش‌بینی زمانی که job فعلی می‌تونه اجرا بشه تا:
                # 1. تکمیلش
                time_to_finish = remaining[current_job['task']]
                # 2. یا release شدن job جدید (اگه هست)
                if job_idx < len(self.jobs):
                    time_to_next_release = self.jobs[job_idx]['release'] - time
                else:
                    time_to_next_release = float('inf')

                delta = min(time_to_finish, time_to_next_release)
                time += delta
                remaining[current_job['task']] -= delta

                if remaining[current_job['task']] == 0:
                    # job تموم شده، حذفش از ready_jobs
                    ready_jobs.remove(current_job)
                    self.schedule.append((current_start, time, current_job['task']))
                    current_job = None
                    current_start = None



    def get_slack_intervals(self):
        slack = []
        if not self.schedule:
            slack.append((0, self.hyperperiod))
            return slack

        self.schedule.sort()
        prev_end = 0
        for start, end, _ in self.schedule:
            if start > prev_end:
                slack.append((prev_end, start))
            prev_end = max(prev_end, end)
        if prev_end < self.hyperperiod:
            slack.append((prev_end, self.hyperperiod))
        return slack

    def schedule_soft_task(self, task, interval):
        start, end = interval
        self.soft_tasks.append(task)
        self.schedule.append((start, start + task.execution, task))
        self.schedule.sort()

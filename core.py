from itertools import chain
from math import gcd
from functools import reduce

from job import Job
import heapq
from itertools import count

class core:
    def __init__(self):
        self.hyperperiod = 0
        self.tasks = []
        self.schedule = []

    def calculate_hyperperiod(self):
        def lcm(a, b):
            return a * b // gcd(a, b)
        periods = [task.period for task in self.tasks]
        if len(periods) != 0:
            self.hyperperiod = reduce(lcm, periods)

    def generate_jobs(self):
        self.jobs = []
        self.jobs = list(chain.from_iterable(
            [
                Job(
                    task_id=task.id,
                    release_time=task.period * i,
                    deadline=task.period * i + task.deadline,
                    wcet=task.wcet
                )
                for i in range(self.hyperperiod // task.period)
            ]
            for task in self.tasks if task.period > 0
        ))

    def edf_schedule(self):
        jobs = self.jobs
        jobs.sort(key=lambda j: j.release_time)
        event_queue = jobs[:]

        ready_queue = []
        self.schedule = []

        time = 0
        current_job = None
        next_release_index = 0
        counter = count()  # شمارنده یکتا برای heapq

        while time < self.hyperperiod or current_job or ready_queue:
            while next_release_index < len(jobs) and jobs[next_release_index].release_time <= time:
                job = jobs[next_release_index]
                heapq.heappush(ready_queue, (job.deadline, next(counter), job))
                next_release_index += 1

            if current_job and ready_queue:
                next_deadline, _, peek_job = ready_queue[0]
                if peek_job.deadline < current_job.deadline:
                    heapq.heappush(ready_queue, (current_job.deadline, next(counter), current_job))
                    current_job = None

            if not current_job and ready_queue:
                _, _, current_job = heapq.heappop(ready_queue)

            if current_job:
                next_event_time = min(
                    jobs[next_release_index].release_time if next_release_index < len(jobs) else self.hyperperiod,
                    time + current_job.remaining_time
                )

                duration = next_event_time - time
                self.schedule.append((time, current_job.task_id, duration))
                current_job.remaining_time -= duration
                time = next_event_time
                if current_job.remaining_time == 0:
                    current_job.finished = True
                    current_job = None
            else:
                if next_release_index < len(jobs):
                    idle_until = jobs[next_release_index].release_time
                    self.schedule.append((time, "IDLE", idle_until - time))
                    time = idle_until
                else:
                    break
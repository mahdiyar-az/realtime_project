from itertools import chain
from math import gcd
from functools import reduce

from job import Job


class core:
    def __init__(self):
        self.hyperperiod = 0
        self.tasks = []

    def calculate_hyperperiod(self):
        def lcm(a, b):
            return a * b // gcd(a, b)
        periods = [task.period for task in self.tasks]
        if len(periods) != 0:
            self.hyperperiod = reduce(lcm, periods)
            print(self.hyperperiod)

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

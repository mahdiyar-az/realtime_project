class Task:
    def __init__(self, id, utilization, wcet, period, deadline, task_type,arrival=0):
        self.id = id
        self.utilization = utilization
        self.wcet = wcet
        self.period = period
        self.deadline = deadline
        self.task_type = task_type  # 'soft' یا 'hard'
        self.arrival_time =arrival
        self.execution = []
class Job:
    def __init__(self, task_id, release_time, deadline, wcet):
        self.task_id = task_id
        self.release_time = release_time
        self.deadline = deadline
        self.remaining_time = wcet
        self.wcet = wcet
        self.finished = False

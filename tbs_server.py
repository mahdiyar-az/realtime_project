class TBSServer:
    def __init__(self, utilization):
        self.us = utilization
        self.last_virtual_deadline = 0
        self.ap_tasks = []

    def add_task(self, task, arrival_time):
        start_time = max(arrival_time, self.last_virtual_deadline)
        virtual_deadline = start_time + (task.wcet / self.us)
        self.last_virtual_deadline = virtual_deadline
        self.ap_tasks.append((task, virtual_deadline))

    def get_scheduled_tasks(self):
        return sorted(self.ap_tasks, key=lambda x: x[1])
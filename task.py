class Task:
    def __init__(self,id, execution, period, deadline, soft=False):
        self.id=id
        self.execution = execution
        self.duration = execution
        self.period = period
        self.deadline = deadline
        self.soft = soft
    def __lt__(self, other):
        return self.deadline < other.deadline

    def utilization(self):
        return self.execution/self.period
    def __repr__(self):
        # return f"{'Soft' if self.soft else 'Hard'}Task(exec={self.execution}, period={self.period}, util={self.execution/self.period})"
        return str(
            {
                "id":self.id,
                "execution": self.execution,
                "duration": self.duration,
                "period": self.period,
                "deadline": self.deadline,
                "type": 'Soft' if self.soft else 'Hard'

            }
        )
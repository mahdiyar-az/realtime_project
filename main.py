from core import core
from uunifast import generate_tasks
from mapper import wfd_mapping, edf_schedule
from tbs_server import TBSServer
import random





ALL_CORES = [8]
EFFICIENCYS = [0.25]
for all_core in ALL_CORES:
    for efficiency in EFFICIENCYS:
        cores = [core() for _ in range(all_core)]
        tasks = generate_tasks(30, all_core, efficiency)

        print(f"\n=== {all_core} CORES | Efficiency {efficiency} ===")

        cores = wfd_mapping(tasks, cores)

        for idx, c in enumerate(cores):
            for idy,a in enumerate(c.tasks):
                print(a.wcet,a.period)
            c.calculate_hyperperiod()
            c.generate_jobs()
            # schedule = edf_schedule(c)


        # گام 3: زمان‌بندی وظایف نرم با TBS
        server = TBSServer(utilization=0.1)
        aperiodic_tasks = [t for t in tasks if t.task_type == 'soft']
        for task in aperiodic_tasks:
            arrival_time = random.randint(0, 100)
            server.add_task(task, arrival_time)

        print("\nTBS Server schedule for soft (aperiodic) tasks:")
        for task, vdl in server.get_scheduled_tasks():
            print(f"  Task {task.id} | WCET={task.wcet} | Virtual Deadline={round(vdl, 2)}")


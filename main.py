from core import core
from uunifast import generate_tasks
from mapper import wfd_mapping
from tbs_server import TBSServer
import random





ALL_CORES = [8, 16, 32]
EFFICIENCYS = [0.25,0.5,0.75,1]
for all_core in ALL_CORES:
    for efficiency in EFFICIENCYS:
        cores = [core() for _ in range(all_core)]
        tasks = generate_tasks(50, all_core, efficiency)

        print(f"\n=== {all_core} CORES | Efficiency {efficiency} ===")

        cores = wfd_mapping(tasks, cores)

        for idx, c in enumerate(cores):
            # print('-----------------------------------------------------------------------')
            # for idy,a in enumerate(c.tasks):
            #     print(a.period,a.wcet)
            print("core ",idx+1)
            c.calculate_hyperperiod()
            c.generate_jobs()
            c.edf_schedule()
            # if idx>0:
            #     continue
            # for idy,b in enumerate(c.schedule):
            #
            #     print(b)






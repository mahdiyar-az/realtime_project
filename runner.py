import json
from core import core
# from cuckoo import cuckoo
# from cuckoo2 import CuckooScheduler
from task import Task
from uunifast import generate_tasks
from mapper import wfd_mapping,sfla
from sbti import sbti_schedule

ALL_CORES = [8, 16, 32]
EFFICIENCYS = [0.25, 0.5, 0.75, 1]

def runner_generate_task():


    for all_core in ALL_CORES:
        for efficiency in EFFICIENCYS:
            tasks = generate_tasks(50, all_core, efficiency)
            output = {
                "tasks":[{'id':t.id,'util':t.execution/t.period,'execution':t.execution,'period':t.period,'deadline':t.deadline,'type':'soft' if t.soft else 'hard'} for t in tasks]
            }
            filename = f"./tasks/task_output_{all_core}cores_{int(efficiency * 100)}.json"
            with open(filename, "w") as f:
                json.dump(output, f, indent=2)

    print("task saved")
def phase1():
    for all_core in ALL_CORES:
        for efficiency in EFFICIENCYS:
            print(f"./tasks/task_output_{all_core}cores_{int(efficiency * 100)}.json")
            soft_tasks =[]
            hard_task =[]
            filename = f"./tasks/task_output_{all_core}cores_{int(efficiency * 100)}.json"
            with open(filename, "r") as f:
                data = json.load(f)

            all_task = data["tasks"]
            for t in all_task:
                if t["type"]=='soft':
                    task = Task(t["id"],t["execution"], t["period"], t["deadline"], True)
                    soft_tasks.append(task)
                else:
                    task = Task(t["id"], t["execution"], t["period"], t["deadline"], False)
                    hard_task.append(task)
            cores = [core() for _ in range(all_core)]

            cores = wfd_mapping(hard_task, cores)

            for c in cores:
                c.calculate_hyperperiod()
                c.generate_jobs()
                c.edf_schedule()


            sbti_schedule(soft_tasks, cores)

            all_task_strs = list({str(t) for t in hard_task + soft_tasks})
            sum_task = sum({t.execution / t.period for t in hard_task})
            output = {
                "config": {
                    "total_cores": all_core,
                    "efficiency": efficiency
                },
                "sum_util_task": sum_task,
                "tasks": all_task_strs,
                "cores": []
            }

            for i, c in enumerate(cores):

                core_info = {
                    "core_id": i,
                    "sum_util_task": sum({t.execution / t.period for t in c.tasks}),
                    "tasks": [str(t) for t in c.tasks],
                    "soft_tasks": [str(t) for t in c.soft_tasks],
                    "schedule":c.schedule

                }
                output["cores"].append(core_info)

            filename = f"./phase1/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json"
            with open(filename, "w") as f:
                json.dump(output, f, indent=2)

            print(f"Output saved to {filename}")

def phase2_hardtask():
    for all_core in ALL_CORES:
        for efficiency in EFFICIENCYS:
            print(f"./tasks/task_output_{all_core}cores_{int(efficiency * 100)}.json")
            soft_tasks = []
            hard_task = []
            filename = f"./tasks/task_output_{all_core}cores_{int(efficiency * 100)}.json"
            with open(filename, "r") as f:
                data = json.load(f)

            all_task = data["tasks"]
            for t in all_task:
                if t["type"] == 'soft':
                    task = Task(t["id"],t["execution"], t["period"], t["deadline"], True)
                    soft_tasks.append(task)
                else:
                    task = Task(t["id"],t["execution"], t["period"], t["deadline"], False)
                    hard_task.append(task)
            cores = [core() for _ in range(all_core)]
            best_assignment = sfla(hard_task, all_core)
            for i,a in enumerate(best_assignment):
                cores[a].add_task(hard_task[i])

            for c in cores:
                c.calculate_hyperperiod()
                c.generate_jobs()
                c.edf_schedule()
            # print(cuckoo(cores,soft_tasks))
            # cuckoo = CuckooScheduler(soft_tasks, cores)
            # best_soft_assignment = cuckoo.schedule()

            # # تخصیص soft taskها به هسته‌ها
            # for task_id, core_id in enumerate(best_soft_assignment):
            #     cores[core_id].add_task(soft_tasks[task_id])
            output = {
                "cores":[]
            }

            for i, c in enumerate(cores):
                core_info = {
                    "core_id": i,
                    "sum_util_task": sum({t.execution/t.period for t in c.tasks}),
                    "tasks": [str(t) for t in c.tasks],
                    "schedule": c.schedule

                }
                output["cores"].append(core_info)
                filename = f"./phase2/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json"
                with open(filename, "w") as f:
                    json.dump(output, f, indent=2)
# runner_generate_task()
# phase1()
phase2_hardtask()
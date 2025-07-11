import json
from core import core
from cuckoo2 import cuckoo
from output_generator import last_exec, power

from task import Task
from uunifast import generate_tasks
from mapper import wfd_mapping,sfla
from sbti import sbti_schedule

ALL_CORES = [8,16,32]
EFFICIENCYS = [1/4,2/4,3/4,4/4]

def runner_generate_task():


    for all_core in ALL_CORES:
        for efficiency in EFFICIENCYS:
            tasks = generate_tasks(50, all_core, efficiency)
            output = {
                "sum_util":sum({t.execution/t.period for t in tasks}),
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
            sum_task = sum({t.execution / t.period for t in hard_task+soft_tasks})
            output = {
                "soft_task":[t.to_dict() for t in soft_tasks],
                "config": {
                    "total_cores": all_core,
                    "efficiency": efficiency
                },
                "sum_util_task": sum_task,
                "sum_util": sum_task,

                "tasks": all_task_strs,
                "cores": []
            }
            for i, c in enumerate(cores):
                core_info = {
                    "core_id": i,
                    "sum_util_task": sum({t.execution / t.period for t in c.tasks}),
                    "tasks": [t.to_dict() for t in c.tasks],
                    "soft_tasks": [t.to_dict() for t in c.soft_tasks],
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
                # print(t)
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

            output = {
                "soft_task":[t.to_dict() for t in soft_tasks],
                "sum_util":0,
                "cores":[]
            }
            a = sum({t.execution/t.period for t in soft_tasks})
            for i, c in enumerate(cores):
                a= a+sum({t.execution/t.period for t in c.tasks})
                core_info = {
                    "core_id": i,
                    "sum_util_task": sum({t.execution/t.period for t in c.tasks}),
                    "hyperperiod":c.hyperperiod,
                    "tasks": [t.to_dict() for t in c.tasks],
                    "schedule": c.schedule

                }
                output["sum_util"]=a
                output["cores"].append(core_info)

                filename = f"./phase2/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json"
                with open(filename, "w") as f:
                    json.dump(output, f, indent=2)

def phase2_softask():
    for all_core in ALL_CORES:
        for efficiency in EFFICIENCYS:
            print(f"./phase2/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json")

            filename = f"./phase2/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json"
            with open(filename, "r") as f:
                data = json.load(f)
            soft_tasks = data["soft_task"]
            cores = data["cores"]
            soft_schedule,drop = cuckoo(cores,soft_tasks)
            for a in soft_schedule:
                # print(a)
                # print(data["cores"])
                data["cores"][a["core_id"]]["tasks"].append(soft_tasks[a["task_id"]-30])
                data["cores"][a["core_id"]]["schedule"].append({
                    "start": a["start"],
                    "end": a["end"],
                    "exec": a["end"]-a["start"],
                    "task_id": a["task_id"]
                })
            data["drop"]=drop
            filename = f"./phase2/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json"
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)

def create_output():
    # failer()
    last_exec()
    power()

# runner_generate_task()
# phase1()
# phase2_hardtask()
# phase2_softask()
create_output()

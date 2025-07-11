import json
import matplotlib.pyplot as plt

ALL_CORES = [8,16,32]
EFFICIENCYS = [1/4,2/4,3/4,4/4]


def last_exec():
    y1 = []
    y2 =[]
    for all_core in ALL_CORES:
        for efficiency in EFFICIENCYS:
            print(f"./phase2/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json")

            filename = f"./phase2/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json"
            with open(filename, "r") as f:
                data = json.load(f)

            ends = [item["end"] for d in data["cores"] for item in d["schedule"]]
            max_end = max(ends)

            y1.append(max_end)
            print(f"./phase1/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json")

            filename = f"./phase1/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json"
            with open(filename, "r") as f:
                data = json.load(f)

            ends = [item["end"] for d in data["cores"] for item in d["schedule"]]
            max_end = max(ends)
            print(max(ends))
            y2.append(max_end)

    x = ["8_0/25", "8_0/5","8_0/75","8_1","16_0/25", "16_0/5","16_0/75","16_1","32_0/25", "32_0/5","32_0/75","32_1"]


    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    axs[0].plot(x, y1, color='blue')
    axs[0].set_title("phase2")
    axs[1].plot(x, y2, color='green')
    axs[1].set_title("phase 1")
    plt.tight_layout()
    plt.savefig("./output/last_exec.png", dpi=300)
    # plt.show()

def power():
    def calculate_core_power(core, V_i=1.2, f_i=2.4, alpha=0.5, C_L=1.0, I_sub=0.1):

        utilization = core['sum_util_task']

        dynamic_power = alpha * C_L * (V_i ** 2) * f_i * utilization

        static_power = I_sub * V_i

        total_power = dynamic_power + static_power

        return {
            'core_id': core['core_id'],
            'total_power': total_power,
            'dynamic_power': dynamic_power,
            'static_power': static_power,
            'voltage': V_i,
            'frequency': f_i,
            'utilization': utilization
        }

    def calculate_task_qos(schedule, task_definitions, x=1.5):
        qos_metrics = {}

        task_executions = {}
        for entry in schedule:
            task_id = entry.get('task_id') or (entry.get('task', {}).get('id') if 'task' in entry else None)
            if task_id is not None:
                if task_id not in task_executions:
                    task_executions[task_id] = []
                task_executions[task_id].append(entry)

        for task_id, executions in task_executions.items():
            if task_id not in task_definitions:
                continue

            task = task_definitions[task_id]
            deadline = task['deadline']
            period = task['period']

            executions.sort(key=lambda x: x['start'])

            missed_deadlines = 0
            total_instances = 0
            utility_sum = 0.0

            for i, exec_entry in enumerate(executions):
                end = exec_entry['end']

                instance_deadline = (i + 1) * period

                if end <= instance_deadline:
                    utility = 1.0
                elif instance_deadline < end <= x * instance_deadline:
                    utility = ((instance_deadline - end) / (instance_deadline * (x - 1))) + 1
                else:
                    utility = 0.0
                    missed_deadlines += 1

                utility_sum += utility
                total_instances += 1

            if total_instances > 0:
                miss_rate = missed_deadlines / total_instances
                avg_utility = utility_sum / total_instances
            else:
                miss_rate = 0.0
                avg_utility = 0.0

            qos_metrics[task_id] = {
                'deadline_miss_rate': miss_rate,
                'average_utility': avg_utility,
                'total_instances': total_instances,
                'missed_instances': missed_deadlines,
                'period': period,
                'deadline': deadline
            }

        return qos_metrics

    def calculate_system_metrics(data, x=1.5):
        task_definitions = {task['id']: task for task in data['soft_task']}
        for core in data['cores']:
            for task in core['tasks']:
                if task['id'] not in task_definitions:
                    task_definitions[task['id']] = task

        power_metrics = []
        total_power = 0.0
        for core in data['cores']:
            core_power = calculate_core_power(core)
            power_metrics.append(core_power)
            total_power += core_power['total_power']

        qos_metrics = {}
        system_utility = 0.0
        total_tasks = 0

        for core in data['cores']:
            core_qos = calculate_task_qos(core['schedule'], task_definitions, x)
            qos_metrics[core['core_id']] = core_qos

            for task_id, metrics in core_qos.items():
                system_utility += metrics['average_utility']
                total_tasks += 1

        avg_system_qos = system_utility / total_tasks if total_tasks > 0 else 0

        return {
            'power_metrics': {
                'total_power': total_power,
                'cores': power_metrics,
                'sum_utilization': data['sum_util']
            },
            'qos_metrics': {
                'average_system_qos': avg_system_qos,
                'cores': qos_metrics
            }
        }

    for all_core in ALL_CORES:
        for efficiency in EFFICIENCYS:
            print(f"./phase2/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json")
            filename = f"./phase2/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json"
            with open(filename) as f:
                data = json.load(f)
            system_metrics = calculate_system_metrics(data)
            filename = f"./output/phase2_output_{all_core}cores_{int(efficiency * 100)}.json"
            with open(filename, "w") as f:
                json.dump(system_metrics, f, indent=2)


            print(f"./phase1/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json")
            filename = f"./phase1/scheduling_output_{all_core}cores_{int(efficiency * 100)}.json"
            with open(filename) as f:
                data = json.load(f)
            system_metrics = calculate_system_metrics(data)

            filename = f"./output/phase1_output_{all_core}cores_{int(efficiency * 100)}.json"
            with open(filename, "w") as f:
                json.dump(system_metrics, f, indent=2)


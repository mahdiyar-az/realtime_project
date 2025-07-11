import json

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


    
with open('phase2/scheduling_output_8cores_50.json') as f:
    data = json.load(f)

system_metrics = calculate_system_metrics(data)

print("System Power Metrics:")
print(f"Total Power: {system_metrics['power_metrics']['total_power']:.2f}W")
print(f"Total Utilization: {system_metrics['power_metrics']['sum_utilization']:.4f}")

print("\nSystem QoS Metrics:")
print(f"Average System QoS (Utility): {system_metrics['qos_metrics']['average_system_qos']:.4f}")

core_0_qos = system_metrics['qos_metrics']['cores'][0]
print("\nQoS Metrics for Core 0 Tasks:")
for task_id, metrics in core_0_qos.items():
    print(f"Task {task_id}:")
    print(f"  Miss Rate: {metrics['deadline_miss_rate']:.2%}")
    print(f"  Avg Utility: {metrics['average_utility']:.4f}")
    print(f"  Instances: {metrics['total_instances']}")
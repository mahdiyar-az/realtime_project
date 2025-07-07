# import json
# from core import core
# from uunifast import generate_tasks
# from mapper import wfd_mapping
# from sbti import sbti_schedule
#
# ALL_CORES = [8, 16, 32]
# EFFICIENCYS = [0.25, 0.5, 0.75, 1]
#
# for all_core in ALL_CORES:
#     for efficiency in EFFICIENCYS:
#         print(f"\n=== {all_core} CORES | Efficiency {efficiency} ===")
#         cores = [core() for _ in range(all_core)]
#
#         tasks = generate_tasks(30, all_core, efficiency)
#         cores = wfd_mapping(tasks, cores)
#
#         for c in cores:
#             c.calculate_hyperperiod()
#             c.generate_jobs()
#             c.edf_schedule()
#
#         soft_tasks = generate_tasks(20, all_core, efficiency, soft=True)
#
#         sbti_schedule(soft_tasks, cores)
#
#         all_task_strs = list({str(t) for t in tasks + soft_tasks})
#         sum_task = sum({t.execution/t.period for t in tasks})
#         output = {
#             "config": {
#                 "total_cores": all_core,
#                 "efficiency": efficiency
#             },
#             "sum_util_task":sum_task,
#             "tasks": all_task_strs,
#             "cores": []
#         }
#
#         for i, c in enumerate(cores):
#
#             core_info = {
#                 "core_id": i,
#                 "sum_util_task": sum({t.execution/t.period for t in c.tasks}),
#                 "tasks": [str(t) for t in c.tasks],
#                 "soft_tasks": [str(t) for t in c.soft_tasks],
#                 "schedule": [
#                     {
#                         "start": s[0],
#                         "end": s[1],
#                         "task": str(s[2])
#                     }
#                     for s in c.schedule
#                 ]
#             }
#             output["cores"].append(core_info)
#
#         filename = f"scheduling_output_{all_core}cores_{int(efficiency*100)}.json"
#         with open(filename, "w") as f:
#             json.dump(output, f, indent=2)
#
#         print(f"Output saved to {filename}")

#move to runner
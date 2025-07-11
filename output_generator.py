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


    # ساخت figure با دو subplot کنار هم
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))  # 1 ردیف، 2 ستون

    # نمودار اول
    axs[0].plot(x, y1, color='blue')
    axs[0].set_title("phase2")

    # نمودار دوم
    axs[1].plot(x, y2, color='green')
    axs[1].set_title("phase 1")

    # فاصله بین نمودارها
    plt.tight_layout()

    # ذخیره کردن تصویر
    plt.savefig("./output/last_exec.png", dpi=300)

    # نمایش نمودار (اختیاری)
    plt.show()
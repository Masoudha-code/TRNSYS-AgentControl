from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "examples" / "pv_battery_case" / "Meta data.xlsx"
OUTPUT_FILE = BASE_DIR / "examples" / "pv_battery_case" / "Meta_data_RuleBased_Result.xlsx"


def run_baseline_processing():
    df = pd.read_excel(INPUT_FILE)
    df.columns = df.columns.str.strip()

    new_grid_usage = []
    battery_output = []

    for _, row in df.iterrows():
        load = row["total_houses_load"]
        pv = row["Total_houses_pv"]
        soc = row["battery_SOC"]
        surplus_ev = row["surplus_to_houses_from_EV"]

        grid_usage = load

        if surplus_ev >= load:
            grid_usage = 0
            battery_used = 0
        else:
            load -= surplus_ev
            grid_usage = load

            if pv >= load:
                grid_usage = 0
                battery_used = 0
            else:
                load -= pv

                if soc > 20:
                    battery_capable = load if load <= (soc * 0.8) else soc * 0.8
                    grid_usage = load - battery_capable if load > battery_capable else 0
                    battery_used = battery_capable
                else:
                    grid_usage = load
                    battery_used = 0

        new_grid_usage.append(grid_usage)
        battery_output.append(battery_used)

    df["grid_usage_rule_based"] = new_grid_usage
    df["battery_output_rule_based"] = battery_output

    df.to_excel(OUTPUT_FILE, index=False)
    print(f"Processed file saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    run_baseline_processing()
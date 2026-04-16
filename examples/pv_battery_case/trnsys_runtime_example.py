import os
import numpy as np
from stable_baselines3 import DQN

thisModule = os.path.splitext(os.path.basename(__file__))[0]


model_path = r"E:\PHD\projects\paper8-Dr. Asadi\AI data\dqn_model_sb3"
model = DQN.load(model_path)

def Initialization(TRNData):
    TRNData[thisModule]["rl_results_history"] = []

def StartTime(TRNData):
    inputs = TRNData[thisModule]["inputs"]
    state = np.array([
        inputs[0],  # TIME
        inputs[1],  # EV_Grid_Usage
        inputs[2],  # PV_Generation
        inputs[3],  # EV_Load
        inputs[4],  # surplus_to_houses_from_EV
        inputs[5],  # EV_Batt_SOC
        inputs[6],  # Num_Ev_Arrivals
        inputs[7],  # total_houses_load
        inputs[8],  # total_surplus
        inputs[9],  # total_deficit
        inputs[10], # total_pool_coverage
        inputs[11], # total_battery_supply
        inputs[12], # battery_SOC
        inputs[13], # houses_grid_usage
        inputs[14]  # Total_houses_pv
    ], dtype=np.float32)

    
    action, _states = model.predict(state, deterministic=True)

    action_map = [0, 0.2, 0.4, 0.6, 0.8]
    battery_capacity = state[12] * 0.8  # battery_SOC * 80%
    battery_used = battery_capacity * action_map[action]

    grid_usage_houses = max(
        state[7] - state[4] - state[14] - battery_used, 0
    )

    TRNData[thisModule]["outputs"][0] = grid_usage_houses
    TRNData[thisModule]["outputs"][1] = battery_used
    TRNData[thisModule]["outputs"][2] = action

    TRNData[thisModule]["rl_results_history"].append({
        "time": state[0],
        "grid_usage_houses": grid_usage_houses,
        "battery_used": battery_used,
        "action_selected": action
    })

def Iteration(TRNData):
    StartTime(TRNData)

def EndOfTimeStep(TRNData):
    pass

def LastCallOfSimulation(TRNData):
    print("✅ Simulation Completed. Final timestep results:")
    print(TRNData[thisModule]["rl_results_history"][-1])

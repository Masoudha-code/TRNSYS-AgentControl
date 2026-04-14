import numpy as np
import pandas as pd
import gymnasium as gym
from gymnasium import spaces


class EnergyEnv(gym.Env):
    metadata = {"render.modes": []}

    def __init__(self, df_in: pd.DataFrame):
        super().__init__()
        self.df = df_in.reset_index(drop=True)
        self.current_step = 0
        self.max_steps = len(self.df) - 1

        self.observation_space = spaces.Box(
            low=0.0,
            high=np.inf,
            shape=(15,),
            dtype=np.float32,
        )

        self.action_space = spaces.Discrete(5)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        return self._get_state(), {}

    def _get_state(self):
        row = self.df.iloc[self.current_step]
        return np.array([
            row["TIME"],
            row["EV_Grid_Usage"],
            row["PV_Generation"],
            row["EV_Load"],
            row["surplus_to_houses_from_EV"],
            row["EV_Batt_SOC"],
            row["Num_Ev_Arrivals"],
            row["total_houses_load"],
            row["total_surplus"],
            row["total_deficit"],
            row["total_battery_supply"],
            row["battery_SOC"],
            row["houses_grid_usage"],
            row["total_remaining_defici"],
            row["Total_houses_pv"],
        ], dtype=np.float32)

    def step(self, action: int):
        row = self.df.iloc[self.current_step]

        load = float(row["total_houses_load"])
        pv = float(row["Total_houses_pv"])
        soc = float(row["battery_SOC"])
        surplus_ev = float(row["surplus_to_houses_from_EV"])

        action_map = [0.0, 0.2, 0.4, 0.6, 0.8]
        battery_capacity = soc * 0.8
        battery_used = battery_capacity * action_map[action]

        remaining_load = max(load - surplus_ev - pv - battery_used, 0.0)
        reward = -remaining_load

        self.current_step += 1
        terminated = self.current_step >= self.max_steps
        truncated = False

        next_state = self._get_state() if not terminated else np.zeros(15, dtype=np.float32)
        info = {
            "battery_used": battery_used,
            "remaining_load": remaining_load,
        }

        return next_state, reward, terminated, truncated, info
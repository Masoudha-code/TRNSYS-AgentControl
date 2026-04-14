from pathlib import Path

import pandas as pd
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.logger import configure
from stable_baselines3.common.monitor import Monitor

from env import EnergyEnv


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "examples" / "pv_battery_case" / "Meta_data_RuleBased_Result.xlsx"
LOG_DIR = BASE_DIR / "logs" / "dqn_run"
EVAL_LOG_DIR = BASE_DIR / "logs" / "eval"
TB_LOG_DIR = BASE_DIR / "logs" / "tb"
MODEL_DIR = BASE_DIR / "models"
BEST_MODEL_DIR = MODEL_DIR / "best"
MODEL_OUT = MODEL_DIR / "dqn_model_sb3"

LOG_DIR.mkdir(parents=True, exist_ok=True)
EVAL_LOG_DIR.mkdir(parents=True, exist_ok=True)
TB_LOG_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
BEST_MODEL_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    df = pd.read_excel(DATA_PATH)
    df.columns = df.columns.str.strip()
    return df


def build_model(train_env):
    model = DQN(
        "MlpPolicy",
        train_env,
        learning_rate=1e-3,
        gamma=0.99,
        buffer_size=100_000,
        batch_size=64,
        target_update_interval=500,
        exploration_initial_eps=1.0,
        exploration_final_eps=0.05,
        exploration_fraction=0.1,
        verbose=1,
        tensorboard_log=str(TB_LOG_DIR),
    )
    return model


def train():
    df = load_data()

    train_env = Monitor(EnergyEnv(df), filename=str(LOG_DIR / "train.monitor.csv"))
    eval_env = Monitor(EnergyEnv(df), filename=str(LOG_DIR / "eval.monitor.csv"))

    model = build_model(train_env)

    logger = configure(str(LOG_DIR), ["stdout", "csv", "tensorboard"])
    model.set_logger(logger)

    eval_callback = EvalCallback(
        eval_env,
        eval_freq=5_000,
        n_eval_episodes=3,
        deterministic=True,
        best_model_save_path=str(BEST_MODEL_DIR),
        log_path=str(EVAL_LOG_DIR),
    )

    model.learn(total_timesteps=200_000, callback=eval_callback)
    model.save(str(MODEL_OUT))

    print(f"Model saved to: {MODEL_OUT}")


if __name__ == "__main__":
    train()
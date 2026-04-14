from pathlib import Path

import pandas as pd


def get_base_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def load_excel_file(file_path: Path) -> pd.DataFrame:
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    return df


def save_excel_file(df: pd.DataFrame, file_path: Path) -> None:
    df.to_excel(file_path, index=False)


def ensure_directory(dir_path: Path) -> None:
    dir_path.mkdir(parents=True, exist_ok=True)
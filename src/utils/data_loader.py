"""Utility: Data loading and preprocessing for battery datasets.
Supports NASA and CALCE dataset formats.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from loguru import logger


def load_battery_csv(filepath: str) -> pd.DataFrame:
    """Load a battery cycle CSV with standard columns."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {filepath}")
    df = pd.read_csv(path)
    logger.info(f"Loaded {len(df)} rows from {path.name}")
    return df


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer features from raw cycle data.
    Expected columns: cycle, voltage, current, temperature, capacity
    """
    features = pd.DataFrame()
    features["cycle"] = df["cycle"]
    features["capacity_fade"] = df["capacity"].max() - df["capacity"]
    features["avg_voltage"] = df.groupby("cycle")["voltage"].transform("mean")
    features["avg_temp"] = df.groupby("cycle")["temperature"].transform("mean")
    features["internal_resistance"] = (
        df["voltage"].diff().abs() / (df["current"].diff().abs() + 1e-9)
    )
    return features.dropna()


def compute_soh(capacity: np.ndarray, nominal_capacity: float) -> np.ndarray:
    """State of Health: ratio of current to nominal capacity (%)."""
    return (capacity / nominal_capacity) * 100

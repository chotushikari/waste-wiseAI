import pandas as pd
from pathlib import Path
from services.config import INVENTORY_PARQUET, INVENTORY_CSV, ACTION_LOG_CSV

def load_inventory(parquet_first: bool = True) -> pd.DataFrame:
    """
    Load inventory data from Parquet (faster) or fallback to CSV.
    """
    try:
        if parquet_first and INVENTORY_PARQUET.exists():
            return pd.read_parquet(INVENTORY_PARQUET)
        return pd.read_csv(INVENTORY_CSV)
    except Exception as e:
        print(f"Error loading inventory: {e}")
        return pd.DataFrame()

def save_inventory(df: pd.DataFrame):
    """
    Save inventory to both Parquet and CSV for fast access + human-readable export.
    """
    try:
        df.to_parquet(INVENTORY_PARQUET, index=False)
        df.to_csv(INVENTORY_CSV, index=False)
    except Exception as e:
        print(f"Error saving inventory: {e}")

def load_action_log() -> pd.DataFrame:
    """
    Load the full action log.
    """
    try:
        return pd.read_csv(ACTION_LOG_CSV, encoding="utf-8")
    except FileNotFoundError:
        return pd.DataFrame(columns=["timestamp", "item_id", "action_type", "quantity", "reason", "value"])
    except Exception as e:
        print(f"Error loading action log: {e}")
        return pd.DataFrame(columns=["timestamp", "item_id", "action_type", "quantity", "reason", "value"])

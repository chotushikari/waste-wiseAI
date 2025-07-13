import pandas as pd
from pathlib import Path
from services.config import INVENTORY_PARQUET, INVENTORY_CSV, ACTION_LOG_CSV

def load_inventory(parquet_first: bool = True) -> pd.DataFrame:
    """
    Load inventory data from Parquet (faster) or fallback to CSV.
    Handles corrupted Parquet files by regenerating them from CSV.
    """
    try:
        if parquet_first and INVENTORY_PARQUET.exists():
            try:
                return pd.read_parquet(INVENTORY_PARQUET)
            except Exception as parquet_error:
                print(f"Parquet file corrupted, falling back to CSV: {parquet_error}")
                # Try to regenerate Parquet from CSV
                try:
                    df = pd.read_csv(INVENTORY_CSV)
                    df.to_parquet(INVENTORY_PARQUET, index=False)
                    print("Parquet file regenerated from CSV successfully")
                    return df
                except Exception as csv_error:
                    print(f"Error reading CSV: {csv_error}")
                    return pd.DataFrame()
        
        # Fallback to CSV
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
    Load the full action log with schema validation and Parquet corruption handling.
    """
    expected_columns = ["timestamp", "item_id", "action_type", "quantity", "reason", "value"]
    try:
        df = pd.read_csv(ACTION_LOG_CSV, encoding="utf-8", low_memory=False)

        # Ensure all expected columns are present
        for col in expected_columns:
            if col not in df.columns:
                df[col] = None

        return df[expected_columns]

    except FileNotFoundError:
        return pd.DataFrame(columns=expected_columns)
    except Exception as e:
        print(f"Error loading action log: {e}")
        return pd.DataFrame(columns=expected_columns)

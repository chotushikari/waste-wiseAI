import pandas as pd
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_dual(df: pd.DataFrame, base_filename: str, folder: str = "data", index: bool = False):
    """Save a DataFrame to both CSV and Parquet formats."""
    os.makedirs(folder, exist_ok=True)
    csv_path = os.path.join(folder, f"{base_filename}.csv")
    parquet_path = os.path.join(folder, f"{base_filename}.parquet")

    try:
        df.to_csv(csv_path, index=index)
        logger.info(f"CSV saved: {csv_path}")
    except Exception as e:
        logger.error(f"CSV save failed: {e}")
        raise

    try:
        df.to_parquet(parquet_path, index=index)
        logger.info(f"Parquet saved: {parquet_path}")
    except Exception as e:
        logger.error(f"Parquet save failed: {e}")
        raise

def generate_sustainability_log(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a sustainability log DataFrame."""
    try:
        top_waste_contributors = df.nlargest(10, 'forecasted_waste_value')[[
            'item_id', 'item_name', 'category', 'forecasted_waste_units', 'forecasted_waste_value'
        ]].assign(tag='🚨 Top Waste Contributors')

        inefficient_items = df.nsmallest(10, 'efficiency_ratio')[[
            'item_id', 'item_name', 'category', 'co2_saved_kg', 'efficiency_ratio'
        ]].assign(tag='⚠️ Inefficient Items')

        top_co2_impact_items = df.nlargest(10, 'co2_saved_kg')[[
            'item_id', 'item_name', 'category', 'co2_saved_kg', 'sustainability_score'
        ]].assign(tag='🌍 Top CO₂ Impact Items')

        return pd.concat([top_waste_contributors, inefficient_items, top_co2_impact_items])

    except Exception as e:
        logger.error(f"Error while generating sustainability log: {e}")
        raise

def save_sustainability_log(df: pd.DataFrame, folder: str = "logs/sustainability", index: bool = False):
    """Save a sustainability log with specific DataFrame transformations."""
    os.makedirs(folder, exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")

    try:
        log_df = generate_sustainability_log(df)
    except Exception as e:
        logger.error(f"Failed to generate sustainability log: {e}")
        raise

    csv_path = os.path.join(folder, f"sustainability_log_{today_str}.csv")
    parquet_path = os.path.join(folder, f"sustainability_log_{today_str}.parquet")

    try:
        log_df.to_csv(csv_path, index=index)
        log_df.to_parquet(parquet_path, index=index)
        logger.info(f"Daily sustainability log saved in CSV and Parquet: {today_str}")
    except Exception as e:
        logger.error(f"Error saving sustainability logs: {e}")
        raise

# scripts/upgrade_action_logs.py

import pandas as pd
import os
from services.config import ACTION_LOG_CSV, ACTION_LOG_PARQUET

# Desired structure
ordered_cols = [
    "timestamp", "item_id", "action_type", "quantity", "reason", "value",
    "current_stock", "days_remaining", "base_price", "dynamic_price",
    "forecasted_waste_units", "forecasted_waste_value", "predicted_daily_sales",
    "co2_saved_kg", "sustainability_score", "efficiency_ratio",
    "recommended_action", "tactical_note", "risk_tag", "date", "category", "department"
]

dtype_casts = {
    "timestamp": str,
    "item_id": str,
    "action_type": str,
    "quantity": int,
    "reason": str,
    "value": float,
    "current_stock": int,
    "days_remaining": int,
    "base_price": float,
    "dynamic_price": float,
    "forecasted_waste_units": int,
    "forecasted_waste_value": float,
    "predicted_daily_sales": float,
    "co2_saved_kg": float,
    "sustainability_score": float,
    "efficiency_ratio": float,
    "recommended_action": str,
    "tactical_note": str,
    "risk_tag": str,
    "date": str,
    "category": str,
    "department": str
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Add any missing columns with default values
    for col in ordered_cols:
        if col not in df.columns:
            df[col] = "" if dtype_casts[col] == str else 0

    # Keep only relevant columns, in order
    df = df[ordered_cols]

    # Cast to proper dtypes
    for col, dtype in dtype_casts.items():
        if dtype in [int, float]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(dtype)
        else:
            df[col] = df[col].astype(str)

    return df

def upgrade_action_logs():
    try:
        updated_df = pd.DataFrame()

        if os.path.exists(ACTION_LOG_CSV):
            print(f"📥 Reading: {ACTION_LOG_CSV}")
            csv_df = pd.read_csv(ACTION_LOG_CSV, dtype=str)
            csv_df = normalize_columns(csv_df)
            updated_df = pd.concat([updated_df, csv_df], ignore_index=True)

        if os.path.exists(ACTION_LOG_PARQUET):
            print(f"📥 Reading: {ACTION_LOG_PARQUET}")
            parquet_df = pd.read_parquet(ACTION_LOG_PARQUET)
            parquet_df = normalize_columns(parquet_df)
            updated_df = pd.concat([updated_df, parquet_df], ignore_index=True)

        if updated_df.empty:
            print("⚠️ No action logs found to upgrade.")
            return

        # Drop duplicates if any
        updated_df.drop_duplicates(inplace=True)

        # Save updated versions
        updated_df.to_csv(ACTION_LOG_CSV, index=False)
        updated_df.to_parquet(ACTION_LOG_PARQUET, index=False)

        print(f"✅ Upgraded action logs with {len(updated_df)} records and saved to both CSV and Parquet.")

    except Exception as e:
        print(f"[❌ Upgrade Error] {e}")

if __name__ == "__main__":
    upgrade_action_logs()

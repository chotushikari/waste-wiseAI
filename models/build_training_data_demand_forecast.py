# # scripts/build_demand_training_data.py

# import pandas as pd
# import os
# from datetime import datetime

# ACTION_LOG_PARQUET = "C:\\wastewiseAi\\data\\actions_log.parquet"
# ACTION_LOG_CSV = "C:\\wastewiseAi\\data\\action_log.csv"

# OUTPUT_PATH = "C:\\wastewiseAi\\data\\action_log_demand_training.csv"

# import pandas as pd

# df = pd.read_parquet("C:\\wastewiseAi\\data\\actions_log.parquet")  # or .parquet if using that
# print(df.columns)
# print(df.head())



# def load_logs():
#     if os.path.exists(ACTION_LOG_PARQUET):
#         print("📂 Loading Parquet log...")
#         return pd.read_parquet(ACTION_LOG_PARQUET)
#     elif os.path.exists(ACTION_LOG_CSV):
#         print("📂 Loading CSV log...")
#         return pd.read_csv(ACTION_LOG_CSV, parse_dates=["timestamp"])
#     else:
#         raise FileNotFoundError("❌ No action log file found! Please run your simulator first.")

# def build_training_data():
#     print("🔍 Loading logs...")
#     logs = load_logs()
#     sales_logs = logs[logs["action_type"] == "sale"].copy()
#     sales_logs["date"] = sales_logs["timestamp"].dt.date

#     print("📊 Aggregating daily sales...")
#     grouped = sales_logs.groupby(["item_id", "date"])["quantity"].sum().reset_index()
#     grouped.rename(columns={"quantity": "sales_today"}, inplace=True)

#     # Load latest inventory snapshot
#     from services.loader import load_inventory
#     inventory = load_inventory()

#     print("🔗 Merging inventory features...")
#     merged = pd.merge(grouped, inventory, on="item_id", how="left")

#     # Feature engineering
#     merged["markdown"] = (merged["base_price"] - merged["dynamic_price"]) / merged["base_price"]

#     features = [
#         "item_id", "date", "sales_today",
#         "base_price", "dynamic_price", "markdown",
#         "predicted_daily_sales", "forecasted_waste_units",
#         "co2_saved_kg", "sustainability_score", "category"
#     ]
#     merged = merged[features].dropna()

#     print(f"💾 Saving training dataset: {OUTPUT_PATH}")
#     os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
#     merged.to_csv(OUTPUT_PATH, index=False)
#     print("✅ Done.")

# if __name__ == "__main__":
#     build_training_data()

import pandas as pd
import os
from datetime import datetime

# Paths (adjust if needed)
INVENTORY_PATH = "data/inventory.parquet"
OUTPUT_TRAINING_DATA_PATH = "data/training_data_demand_forecast.csv"

# === CONFIG ===
TARGET_COLUMN = "predicted_daily_sales"
EXCLUDED_COLUMNS = [
    "item_id", "item_name", "daily_sales", "predicted_monthly_sales",
    "last_restock_date", "next_restock_date", "tactical_note", "confidence", "risk_tag"
]

# === LOAD DATA ===
def load_inventory():
    print("🔍 Loading Inventory...")
    return pd.read_parquet(INVENTORY_PATH)

# === CLEAN & PREPARE ===
def prepare_training_data(df: pd.DataFrame) -> pd.DataFrame:
    print("⚙️ Preparing features...")

    # Drop rows with missing target
    df = df.dropna(subset=[TARGET_COLUMN])

    # Drop unwanted columns
    X = df.drop(columns=[col for col in EXCLUDED_COLUMNS if col in df.columns])

    # Handle categoricals manually for XGBoost
    for col in ["category", "department", "recommended_action"]:
        if col in X.columns:
            X[col] = X[col].astype(str)
            X[col] = X[col].fillna("Unknown")
            X[col] = X[col].astype("category").cat.codes

    # Remove any remaining NaNs
    X = X.fillna(0)
    return X

# === SAVE TRAINING DATA ===
def save_training_data(df: pd.DataFrame):
    df.to_csv(OUTPUT_TRAINING_DATA_PATH, index=False)
    print(f"✅ Training data saved to: {OUTPUT_TRAINING_DATA_PATH}")

# === MAIN ===
def build_training_data():
    df = load_inventory()
    training_data = prepare_training_data(df)
    save_training_data(training_data)

if __name__ == "__main__":
    build_training_data()

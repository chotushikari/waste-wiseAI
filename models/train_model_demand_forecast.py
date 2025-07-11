# models/train_model_demand_forecast.py

import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# === CONFIG ===
TRAINING_DATA_PATH = "data/training_data_demand_forecast.csv"
MODEL_OUTPUT_PATH = "models/demand_forecast_model.pkl"

# === LOAD DATA ===
print("📂 Loading training data...")
df = pd.read_csv(TRAINING_DATA_PATH)

# === FEATURES & TARGET ===
X = df.drop(columns=["predicted_daily_sales"])
y = df["predicted_daily_sales"]

# === TRAIN-TEST SPLIT ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# === MODEL ===
model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.9,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42
)

print("🚀 Training XGBoost Regressor...")
model.fit(X_train, y_train)

# === EVALUATE ===
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n📊 Model Performance:")
print(f"  - Mean Squared Error: {mse:.2f}")
print(f"  - R2 Score: {r2:.4f}")

# === SAVE MODEL ===
os.makedirs("models", exist_ok=True)
joblib.dump(model, MODEL_OUTPUT_PATH)
print(f"\n✅ Model saved at: {MODEL_OUTPUT_PATH}")

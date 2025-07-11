# models/train_demand_forecast.py

import pandas as pd
import numpy as np
import joblib
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import os

# === 1. Load Historical Data ===
data_path = "C:\\wastewiseAi\\data\\training_data_demand_forecast.csv"  # Ensure this file exists
if not os.path.exists(data_path):
    raise FileNotFoundError("Historical demand training file not found!")

df = pd.read_csv(data_path)

# === 2. Preprocessing ===
# Fill missing values
numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

# Encode markdown levels (if any)
if "recommended_action" in df.columns:
    df["markdown_level"] = df["recommended_action"].map({
        "NO ACTION": 0,
        "MARKDOWN -10%": 10,
        "MARKDOWN -30%": 30,
        "DONATE": 0,
        "RETURN to Supplier": 0
    }).fillna(0)
else:
    df["markdown_level"] = 0

# Encode category (can replace with one-hot if needed)
if "category" in df.columns:
    df["category_encoded"] = df["category"].astype("category").cat.codes
else:
    df["category_encoded"] = 0

# === 3. Features and Target ===
features = [
    "current_stock", "base_price", "dynamic_price", "days_remaining",
    "elasticity", "forecasted_waste_units", "co2_saved_kg",
    "sustainability_score", "markdown_level", "category_encoded"
]
target = "sales_today"

X = df[features]
y = df[target]

# === 4. Train/Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === 5. Train Model ===
model = XGBRegressor(n_estimators=300, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# === 6. Evaluate ===
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n📈 Model Evaluation:")
print(f"RMSE: {rmse:.2f}")
print(f"R^2 Score: {r2:.3f}")

# === 7. Save Model ===
os.makedirs("models", exist_ok=True)
model_path = "models/demand_forecast_model.pkl"
joblib.dump(model, model_path)
print(f"\n✅ Demand Forecast Model saved at: {model_path}")

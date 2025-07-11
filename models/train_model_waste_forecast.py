import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
from joblib import dump

print("📂 Loading training data...")
df = pd.read_parquet("C:\\wastewiseAi\\data\\actions_log.parquet")

# Drop rows missing target
df = df.dropna(subset=["forecasted_waste_units"])

# Drop non-feature columns if they exist
drop_cols = [
    "forecasted_waste_units", "item_id", "item_name", "date",
    "tactical_note", "recommended_action"
]
X = df.drop(columns=[col for col in drop_cols if col in df.columns])
y = df["forecasted_waste_units"]

# 💡 Convert all object columns to category (required by XGBoost with enable_categorical=True)
for col in X.select_dtypes(include="object").columns:
    X[col] = X[col].astype("category")

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("🚀 Training XGBoost Regressor...")
model = XGBRegressor(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    enable_categorical=True,  # ✅ Required when using category types
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n📊 Model Performance:")
print(f"  - Mean Squared Error: {mse:.2f}")
print(f"  - R2 Score: {r2:.4f}")

# Save model
dump(model, "models/waste_forecast_model.pkl")
print("✅ Model saved at: models/waste_forecast_model.pkl")

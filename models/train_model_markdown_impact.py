import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
from joblib import dump

# --- Paths ---
DATA_PATH = Path("data/actions_log.parquet")
MODEL_PATH = Path("models/markdown_impact_model.pkl")

# --- Load Dataset ---
df = pd.read_parquet(DATA_PATH)

# --- Clean & Prepare ---
df = df.dropna(subset=["forecasted_waste_value"])  # Target variable
drop_cols = ["forecasted_waste_value", "item_id", "item_name", "date", "tactical_note", "recommended_action"]

X = df.drop(columns=[col for col in drop_cols if col in df.columns])
y = df["forecasted_waste_value"]

# Convert object columns to category
for col in X.select_dtypes(include="object").columns:
    X[col] = X[col].astype("category")

# --- Train/Test Split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- Train Model ---
model = XGBRegressor(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    enable_categorical=True,
    random_state=42
)
model.fit(X_train, y_train)

# --- Evaluate ---
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# --- Save Model ---
dump(model, MODEL_PATH)

print("✅ Markdown Impact Model Trained")
print(f"📊 Mean Squared Error: {mse:.2f}")
print(f"📈 R2 Score: {r2:.4f}")
print(f"💾 Saved model at: {MODEL_PATH}")

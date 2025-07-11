from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier, Pool
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

# Define the path to the data file
data_dir = Path("data")
actions_log_path = data_dir / "actions_log.parquet"

# Check if the file exists
if not actions_log_path.exists():
    raise FileNotFoundError(f"The file {actions_log_path} does not exist.")

# Load your data
df = pd.read_parquet(actions_log_path)

# Drop any rows with missing values in features or target
df = df.dropna(subset=[
    "recommended_action", "current_stock", "days_remaining", "base_price", "dynamic_price",
    "forecasted_waste_units", "predicted_daily_sales", "co2_saved_kg", "department"
])

# Define features and target
features = [
    "current_stock", "days_remaining", "base_price", "dynamic_price",
    "forecasted_waste_units", "predicted_daily_sales", "co2_saved_kg", "department"
]
target = "recommended_action"
X = df[features]
y = df[target]

# Categorical column
cat_features = ["department"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

# Create CatBoost pools
train_pool = Pool(X_train, y_train, cat_features=cat_features)
test_pool = Pool(X_test, y_test, cat_features=cat_features)

# Train the model
model = CatBoostClassifier(
    iterations=500,
    learning_rate=0.05,
    depth=6,
    loss_function='MultiClass',
    random_seed=42,
    verbose=100
)
model.fit(train_pool)

# Evaluate
y_pred = model.predict(test_pool).flatten()
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))
print("\n📉 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Feature Importance
print("\n📌 Feature Importance:")
print(model.get_feature_importance(prettified=True))

# Save the model
models_dir = Path("models")
models_dir.mkdir(parents=True, exist_ok=True)
model_path = models_dir / "ai_recommendation_model.pkl"
joblib.dump(model, model_path)

print(f"\n✅ Model saved at: {model_path}")

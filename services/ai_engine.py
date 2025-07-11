from joblib import load

# Load trained models
recommendation_model = load("models/ai_recommendation_model.pkl")
demand_model = load("models/demand_forecast_model.pkl")
waste_model = load("models/waste_forecast_model.pkl")
markdown_model = load("models/markdown_impact_model.pkl")

def generate_ai_decision(row):
    features = row[[
        "days_remaining", "current_stock", "co2_saved_kg",
        "forecasted_waste_units", "predicted_daily_sales",
        "dynamic_price", "department", "base_price"
    ]].copy()

    # Ensure categorical features are handled
    for col in features.select_dtypes(include="object").columns:
        features[col] = features[col].astype("category")

    prediction = recommendation_model.predict(features.to_frame().T)[0]
    return prediction

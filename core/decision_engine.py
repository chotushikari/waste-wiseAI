# # core/decision_engine.py

# import pandas as pd
# from services.loader import load_inventory, save_inventory, log_action
# from core.waste_intelligence import enrich_inventory
# from datetime import datetime


# # Configurable thresholds for risk evaluation
# RISK_THRESHOLDS = {
#     "high": 80,
#     "medium": 60,
#     "low": 30
# }

# ACTION_PRIORITIES = [
#     "DONATE", "RETURN", "MARKDOWN_30", "MARKDOWN_10", "NO_ACTION"
# ]


# def get_spoilage_value(row):
#     """
#     Calculate projected ₹ value of units that will spoil before sale
#     """
#     days_left = row['days_remaining']
#     daily_sales = max(row['daily_sales'], 1)
#     projected_sales = min(row['current_stock'], days_left * daily_sales)
#     expected_waste_units = max(row['current_stock'] - projected_sales, 0)
#     return expected_waste_units * row['base_price']


# def determine_final_action(row):
#     """
#     Robust business logic to recommend best action based on:
#     - Risk Score
#     - Spoilage ₹ Value
#     - Days remaining
#     - Sustainability tradeoff (carbon impact)
#     - Overstock condition
#     """
#     risk = row['risk_score']
#     spoilage_val = row['forecasted_waste_value']
#     days = row['days_remaining']
#     carbon = row['carbon_score']
#     overstock = row['current_stock'] > 5 * max(row['daily_sales'], 1)

#     if days <= 1 and spoilage_val > 100:
#         return "DONATE"
#     elif risk > RISK_THRESHOLDS['high'] and overstock:
#         return "RETURN"
#     elif risk > RISK_THRESHOLDS['high']:
#         return "MARKDOWN_30"
#     elif RISK_THRESHOLDS['medium'] < risk <= RISK_THRESHOLDS['high']:
#         return "MARKDOWN_10"
#     elif spoilage_val > 75:
#         return "MARKDOWN_10"
#     else:
#         return "NO_ACTION"


# def run_decision_engine():
#     """
#     - Load inventory
#     - Enrich with waste intelligence
#     - For each SKU, decide best action
#     - Log decision
#     - Save updated inventory
#     - Returns enriched decision inventory
#     """
#     df = load_inventory()
#     enriched = enrich_inventory(df)

#     actions = []
#     for idx, row in enriched.iterrows():
#         action = determine_final_action(row)
#         enriched.at[idx, 'final_action'] = action

#         # Log actionable steps only
#         if action != "NO_ACTION":
#             log_action(
#                 sku=row['item_id'],
#                 action_type=action.lower(),
#                 quantity=row['forecasted_waste_units'],
#                 reason="Auto Recommendation via Decision Engine",
#                 value_saved=row['forecasted_waste_value']
#             )

#         actions.append(action)

#     enriched['final_action'] = actions
#     save_inventory(enriched)
#     return enriched


# if __name__ == "__main__":
#     final_df = run_decision_engine()
#     print("\n🧠 Decision Engine Complete — Daily Recommendations Ready")
#     print(final_df[['item_id', 'item_name', 'risk_score', 'risk_tag', 'forecasted_waste_units', 'forecasted_waste_value', 'recommended_action', 'final_action']].head())

# # core/decision_engine.py

# import pandas as pd
# from services.loader import load_inventory, save_inventory
# from core.waste_intelligence import enrich_inventory
# from core.sustainability import enrich_sustainability

# # Optional (for later Groq + LangChain)
# # from agents.genai_agent import generate_natural_language_recommendation

# def generate_daily_decisions(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()
#     tactical_notes = []

#     for _, row in df.iterrows():
#         decision = row['recommended_action']
#         co2 = row['co2_saved_kg']
#         spoilage_val = row['forecasted_waste_value']
#         score = row['risk_score']
#         tag = row['risk_tag']
#         efficiency = co2 / (spoilage_val + 1e-6)  # avoid divide by zero

#         note = ""

#         if decision == "DONATE":
#             note = f"🔥 Donate to NGO today to avoid ₹{spoilage_val} loss and {round(co2,2)}kg CO₂ waste."
#         elif decision == "MARKDOWN -30%":
#             note = f"📉 Apply -30% markdown. Waste risk is {tag}."
#         elif decision == "MARKDOWN -10%":
#             note = f"📉 Gentle markdown recommended. Stock high, days low."
#         elif decision == "RETURN to Supplier":
#             note = f"↩️ Consider returning stock. ₹{spoilage_val} at risk."
#         else:
#             note = "✅ Stable – No urgent action required."

#         # Sustainability boost: Flag good practices
#         if efficiency > 0.75 and co2 > 2:
#             note += " ✅ High sustainability value in action."

#         tactical_notes.append(note)

#     df["tactical_note"] = tactical_notes
#     return df


# def summarize_decisions(df: pd.DataFrame) -> dict:
#     """
#     Aggregated KPIs for dashboard or AI summary
#     """
#     summary = {
#         "total_items": len(df),
#         "high_risk_items": int((df["risk_score"] > 75).sum()),
#         "total_spoilage_forecast_₹": round(df["forecasted_waste_value"].sum(), 2),
#         "total_meals_saved": int(df["meals_saved"].sum()),
#         "co2_saved_kg": round(df["co2_saved_kg"].sum(), 2),
#         "water_liters_saved": int(df["water_saved_liters"].sum()),
#         "actions_today": df["recommended_action"].value_counts().to_dict()
#     }
#     return summary


# def run_decision_engine(save: bool = True) -> tuple[pd.DataFrame, dict]:
#     """
#     1. Loads inventory
#     2. Enriches with risk, waste, sustainability
#     3. Adds tactical decisions and insights
#     4. Saves updated inventory
#     5. Returns enriched data + summary
#     """
#     df = load_inventory()
#     df = enrich_inventory(df)
#     df = enrich_sustainability(df)
#     df = generate_daily_decisions(df)

#     summary = summarize_decisions(df)

#     if save:
#         save_inventory(df)

#     return df, summary


# if __name__ == "__main__":
#     enriched_df, summary = run_decision_engine()
#     print("\n✅ Decision Engine Executed:")
#     print(enriched_df[["item_id", "item_name", "recommended_action", "tactical_note"]].head())
#     print("\n📊 Summary:")
#     for k, v in summary.items():
#         print(f"{k}: {v}")

# # core/decision_engine.py

# import pandas as pd
# from services.loader import load_inventory, save_inventory
# from core.waste_intelligence import enrich_inventory
# from core.sustainability import enrich_sustainability

# # === TACTICAL DECISION GENERATOR ===
# def generate_daily_decisions(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()
#     tactical_notes = []
#     confidence_levels = []
#     overstock_scores = []

#     for _, row in df.iterrows():
#         decision = row['recommended_action']
#         co2 = row.get('co2_saved_kg', 0.0)
#         spoilage_val = row.get('forecasted_waste_value', 0.0)
#         score = row.get('risk_score', 0.0)
#         tag = row.get('risk_tag', '')
#         days_remaining = row.get('days_remaining', 0)
#         shelf_life = row.get('shelf_life_days', 1)
#         stock = row.get('current_stock', 0)
#         daily_sales = max(row.get('daily_sales', 1), 1)

#         spoilage_pct = min(1.0, spoilage_val / (stock * row.get('base_price', 1) + 1e-6))
#         overstock = stock / daily_sales
#         overstock_scores.append(round(overstock, 2))
#         efficiency = co2 / (spoilage_val + 1e-6)

#         note = ""

#         if decision == "DONATE":
#             note = f"🔥 Donate to NGO today to avoid ₹{spoilage_val:.2f} loss and {round(co2,2)}kg CO₂ waste."
#         elif decision == "MARKDOWN -30%":
#             note = f"📉 Apply -30% markdown. Waste risk is {tag}."
#         elif decision == "MARKDOWN -10%":
#             note = f"📉 Gentle markdown recommended. Stock high, days low."
#         elif decision == "RETURN to Supplier":
#             note = f"↩️ Consider returning stock. ₹{spoilage_val:.2f} at risk."
#         else:
#             note = "✅ Stable – No urgent action required."

#         # Add sustainability bonus flag
#         if efficiency > 0.75 and co2 > 2:
#             note += " ✅ High sustainability impact."

#         # Add confidence label
#         if score > 80 or spoilage_pct > 0.4:
#             confidence = "✅ Confident action"
#         elif 50 < score <= 80:
#             confidence = "⚠️ Moderate confidence"
#         else:
#             confidence = "🟢 Low risk zone"

#         confidence_levels.append(confidence)
#         tactical_notes.append(note)

#     df["tactical_note"] = tactical_notes
#     df["confidence"] = confidence_levels
#     df["overstock_score"] = overstock_scores
#     return df

# # === SUMMARY AGGREGATOR ===
# def summarize_decisions(df: pd.DataFrame) -> dict:
#     return {
#         "total_items": len(df),
#         "high_risk_items": int((df["risk_score"] > 75).sum()),
#         "total_spoilage_forecast_₹": round(df["forecasted_waste_value"].sum(), 2),
#         "total_meals_saved": int(df.get("meals_saved", pd.Series([0]*len(df))).sum()),
#         "co2_saved_kg": round(df.get("co2_saved_kg", pd.Series([0]*len(df))).sum(), 2),
#         "water_liters_saved": int(df.get("water_saved_liters", pd.Series([0]*len(df))).sum()),
#         "actions_today": df["recommended_action"].value_counts().to_dict()
#     }

# # === MAIN EXECUTION WRAPPER ===
# def run_decision_engine(save: bool = True) -> tuple[pd.DataFrame, dict]:
#     df = load_inventory()
#     df = enrich_inventory(df)
#     df = enrich_sustainability(df)
#     df = generate_daily_decisions(df)
#     summary = summarize_decisions(df)
#     if save:
#         save_inventory(df)
#     return df, summary

# if __name__ == "__main__":
#     enriched_df, summary = run_decision_engine()
#     print("\n✅ Decision Engine Executed:")
#     print(enriched_df[["item_id", "item_name", "recommended_action", "tactical_note", "confidence"]].head())
#     print("\n📊 Summary:")
#     for k, v in summary.items():
#         print(f"{k}: {v}")

# core/decision_engine.py

import pandas as pd
from services.loader import load_inventory, save_inventory
from core.waste_intelligence import enrich_inventory
from core.sustainability import enrich_sustainability

# === Tactical Decision Generator ===
def generate_daily_decisions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    tactical_notes, confidence_levels, overstock_scores = [], [], []

    for row in df.itertuples(index=False):
        decision = row.recommended_action
        co2 = getattr(row, 'co2_saved_kg', 0.0)
        spoilage_val = getattr(row, 'forecasted_waste_value', 0.0)
        risk = getattr(row, 'risk_score', 0.0)
        tag = getattr(row, 'risk_tag', '')
        stock = getattr(row, 'current_stock', 0)
        base_price = getattr(row, 'base_price', 1)
        dynamic_price = getattr(row, 'dynamic_price', base_price)  # Use dynamic_price
        daily_sales = max(getattr(row, 'daily_sales', 1), 1)

        spoilage_pct = min(1.0, spoilage_val / ((stock * base_price) + 1e-6))
        overstock = stock / daily_sales
        overstock_scores.append(round(overstock, 2))
        efficiency = co2 / (spoilage_val + 1e-6)

        # Calculate markdown percentage based on dynamic_price
        markdown_pct = ((base_price - dynamic_price) / base_price) * 100 if base_price > 0 else 0

        # Tactical Notes
        # Tactical Notes
        if decision == "DONATE":
            note = f"Action: Donate. Potential savings: ${spoilage_val:.2f}, CO₂ reduction: {round(co2, 2)}kg."
        elif decision == "Strategic Discount - Tier 1":
            note = f"Action: Apply Tier 1 Strategic Discount. New price: ${dynamic_price:.2f} ({markdown_pct:.1f}% reduction). Risk factor: {tag}."
        elif decision == "Strategic Discount - Tier 2":
            note = f"Action: Apply Tier 2 Strategic Discount. New price: ${dynamic_price:.2f} ({markdown_pct:.1f}% reduction). Addressing overstock."
        elif decision == "RETURN to Supplier":
            note = f"Action: Return to supplier. Potential loss avoided: ${spoilage_val:.2f}."
        else:
            note = "Status: Stable. No action required."

        # Sustainability Bonus
        if efficiency > 0.75 and co2 > 2:
            note += " 🌱 High sustainability impact."

        # Confidence Level
        if risk > 80 or spoilage_pct > 0.4:
            confidence = "✅ Confident action"
        elif risk > 50:
            confidence = "⚠️ Moderate confidence"
        else:
            confidence = "🟢 Low risk zone"

        tactical_notes.append(note)
        confidence_levels.append(confidence)

    df["tactical_note"] = tactical_notes
    df["confidence"] = confidence_levels
    df["overstock_score"] = overstock_scores
    return df


# === Summary Aggregator ===
def summarize_decisions(df: pd.DataFrame) -> dict:
    return {
        "total_items": len(df),
        "high_risk_items": int((df["risk_score"] > 75).sum()),
        "total_spoilage_forecast_$": round(df["forecasted_waste_value"].sum(), 2),
        "total_meals_saved": int(df.get("meals_saved", pd.Series(0, index=df.index)).sum()),
        "co2_saved_kg": round(df.get("co2_saved_kg", pd.Series(0.0, index=df.index)).sum(), 2),
        "water_liters_saved": int(df.get("water_saved_liters", pd.Series(0, index=df.index)).sum()),
        "actions_today": df["recommended_action"].value_counts().to_dict()
    }


# === Main Execution Engine ===
def run_decision_engine(save: bool = True) -> tuple[pd.DataFrame, dict]:
    df = load_inventory()
    df = enrich_inventory(df)
    df = enrich_sustainability(df)
    df = generate_daily_decisions(df)
    summary = summarize_decisions(df)

    if save:
        save_inventory(df)

    return df, summary


# === CLI Test ===
if __name__ == "__main__":
    enriched_df, summary = run_decision_engine()

    print("\n✅ Decision Engine Executed:")
    print(enriched_df[[
        "item_id", "item_name", "recommended_action", 
        "tactical_note", "confidence"
    ]].head())

    print("\n📊 Summary:")
    for k, v in summary.items():
        print(f"{k}: {v}")

# import pandas as pd
# import joblib
# import logging
# from services.loader import load_inventory, save_inventory
# from core.waste_intelligence import enrich_inventory
# from core.sustainability import enrich_sustainability
# from sklearn.preprocessing import LabelEncoder

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load Models
# try:
#     waste_model = joblib.load("models/waste_forecast_model.pkl")
#     value_model = joblib.load("models/markdown_impact_model.pkl")
#     recommend_model = joblib.load("models/ai_recommendation_model.pkl")
#     logger.info("Models loaded successfully.")
# except Exception as e:
#     logger.error(f"Error loading models: {e}")
#     raise

# logger.info(waste_model.feature_names_in_)

# def prepare_features_for_model(df: pd.DataFrame) -> pd.DataFrame:
#     # Copy the DataFrame to avoid modifying the original
#     features = df.copy()

#     # Ensure all categorical values are strings before encoding
#     for col in ['risk_tag', 'category', 'department']:
#         features[col] = features[col].astype(str).fillna("unknown")

#     # Apply Label Encoding
#     for col in ['risk_tag', 'category', 'department']:
#         le = LabelEncoder()
#         features[col] = le.fit_transform(features[col])

#     # Ensure all dtypes are numeric
#     return features.astype(float)

# def generate_daily_decisions(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()

#     # Rename columns to match expected feature names
#     df = df.rename(columns={'forecasted_waste_value': 'forecasted_waste_units'})

#     # Prepare features for the model
#     features = prepare_features_for_model(df[['current_stock', 'days_remaining', 'base_price', 'dynamic_price',
#                                               'forecasted_waste_units', 'predicted_daily_sales', 'co2_saved_kg',
#                                               'sustainability_score', 'efficiency_ratio', 'risk_tag', 'category',
#                                               'department']])

#     # Debugging: Check the shape and type of features
#     logger.info(f"Features shape: {features.shape}")
#     logger.info(f"Features dtypes: {features.dtypes}")

#     # Predict using AI models
#     try:
#         df["forecasted_waste_units"] = waste_model.predict(features).round().astype(int)
#         df["forecasted_waste_value"] = value_model.predict(features).round(2)
#         df["recommended_action"] = recommend_model.predict(features)
#     except Exception as e:
#         logger.error(f"Error during model prediction: {e}")
#         raise

#     # Decision Intelligence
#     tactical_notes, confidence_levels, overstock_scores = [], [], []

#     for row in df.itertuples(index=False):
#         decision = row.recommended_action
#         co2 = getattr(row, 'co2_saved_kg', 0.0)
#         spoilage_val = getattr(row, 'forecasted_waste_value', 0.0)
#         risk = getattr(row, 'risk_score', 0.0)
#         tag = getattr(row, 'risk_tag', '')
#         stock = getattr(row, 'current_stock', 0)
#         base_price = getattr(row, 'base_price', 1)
#         daily_sales = max(getattr(row, 'daily_sales', 1), 1)
#         spoilage_pct = min(1.0, spoilage_val / ((stock * base_price) + 1e-6))
#         overstock = stock / daily_sales
#         overstock_scores.append(round(overstock, 2))
#         efficiency = co2 / (spoilage_val + 1e-6)

#         # Tactical Notes
#         if decision == "DONATE":
#             note = f"🔥 Donate to NGO – Save ${spoilage_val:.2f}, avoid {round(co2, 2)}kg CO₂."
#         elif decision == "MARKDOWN -30%":
#             note = f"📉 Apply -30% markdown. Waste risk: {tag}."
#         elif decision == "MARKDOWN -10%":
#             note = f"📉 Gentle markdown. Overstock + approaching expiry."
#         elif decision == "RETURN to Supplier":
#             note = f"↩️ Consider supplier return. Value at risk: ${spoilage_val:.2f}."
#         else:
#             note = "✅ Stable – No urgent action."

#         # Sustainability Bonus
#         if efficiency > 0.75 and co2 > 2:
#             note += " 🌱 High sustainability impact."

#         # Confidence Level
#         if risk > 80 or spoilage_pct > 0.4:
#             confidence = "✅ Confident action"
#         elif risk > 50:
#             confidence = "⚠️ Moderate confidence"
#         else:
#             confidence = "🟢 Low risk zone"

#         tactical_notes.append(note)
#         confidence_levels.append(confidence)

#     df["tactical_note"] = tactical_notes
#     df["confidence"] = confidence_levels
#     df["overstock_score"] = overstock_scores

#     return df

# def summarize_decisions(df: pd.DataFrame) -> dict:
#     return {
#         "total_items": len(df),
#         "high_risk_items": int((df["risk_score"] > 75).sum()),
#         "total_spoilage_forecast_$": round(df["forecasted_waste_value"].sum(), 2),
#         "total_meals_saved": int(df.get("meals_saved", pd.Series(0, index=df.index)).sum()),
#         "co2_saved_kg": round(df.get("co2_saved_kg", pd.Series(0.0, index=df.index)).sum(), 2),
#         "water_liters_saved": int(df.get("water_saved_liters", pd.Series(0, index=df.index)).sum()),
#         "actions_today": df["recommended_action"].value_counts().to_dict()
#     }

# def run_decision_engine(save: bool = True) -> tuple[pd.DataFrame, dict]:
#     try:
#         df = load_inventory()
#         df = enrich_inventory(df)
#         df = enrich_sustainability(df)
#         df = generate_daily_decisions(df)
#         summary = summarize_decisions(df)
#         if save:
#             save_inventory(df)
#         return df, summary
#     except Exception as e:
#         logger.error(f"Error in decision engine execution: {e}")
#         raise

# if __name__ == "__main__":
#     try:
#         enriched_df, summary = run_decision_engine()
#         logger.info("\n✅ Decision Engine Executed:")
#         logger.info(enriched_df[[
#             "item_id", "item_name", "recommended_action",
#             "tactical_note", "confidence"
#         ]].head())
#         logger.info("\n📊 Summary:")
#         for k, v in summary.items():
#             logger.info(f"{k}: {v}")
#     except Exception as e:
#         logger.error(f"Error during CLI execution: {e}")

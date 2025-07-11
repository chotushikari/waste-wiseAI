import os
import requests
import pandas as pd

# --- DEFAULTS ---
DEFAULTS = {
    "co2_per_unit": 1.2,         # kg
    "water_liters_per_unit": 50,
    "energy_kwh_per_unit": 0.25,
    "meals_per_unit": 1 / 0.3,   # 300g per meal
}

CATEGORY_DEFAULTS = {
    "meat":        {"co2": 5.0, "water": 2500, "energy": 1.0},
    "dairy":       {"co2": 3.0, "water": 1000, "energy": 0.5},
    "produce":     {"co2": 0.5, "water": 100,  "energy": 0.1},
    "baked_goods": {"co2": 1.8, "water": 300,  "energy": 0.3},
    "beverages":   {"co2": 0.8, "water": 120,  "energy": 0.2},
    "frozen":      {"co2": 2.5, "water": 800,  "energy": 0.6},
    "household":   {"co2": 1.0, "water": 100,  "energy": 0.2},
}

API_KEY = os.getenv("CLIMATIQ_API_KEY")
CLIMATIQ_ENDPOINT = "https://beta3.api.climatiq.io/estimate"

# --- HELPERS ---
def get_category_defaults(row):
    category = str(row.get("category", "")).lower()
    return CATEGORY_DEFAULTS.get(category, {})

def call_climatiq_api(row):
    if not API_KEY:
        return None
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        payload = {
            "emission_factor": {
                "activity_id": "retail-food_grocery",
                "source": "eea",
                "region": "IN",
                "year": 2022
            },
            "parameters": {
                "money": row.get("base_price", 1.0),
                "money_unit": "inr"
            }
        }
        response = requests.post(CLIMATIQ_ENDPOINT, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("co2e", None)
    except Exception as e:
        print(f"[❌ Climatiq API error] {e} — item: {row.get('item_id', 'UNKNOWN')}")
    return None

def estimate_all(row):
    try:
        units = row.get("forecasted_waste_units", 0)
        base_price = row.get("base_price", 1)
        category = get_category_defaults(row)

        co2_per_unit = (
            call_climatiq_api(row) or
            row.get("carbon_score") or
            category.get("co2") or
            DEFAULTS["co2_per_unit"]
        )
        water = category.get("water") or DEFAULTS["water_liters_per_unit"]
        energy = category.get("energy") or DEFAULTS["energy_kwh_per_unit"]
        meals = units * DEFAULTS["meals_per_unit"]

        co2_total = units * co2_per_unit
        water_total = units * water
        energy_total = units * energy

        score = (
            0.4 * min(co2_total / 5, 1.0) +
            0.3 * min(water_total / 2000, 1.0) +
            0.2 * min(energy_total / 1.0, 1.0) +
            0.1 * min(meals / 10, 1.0)
        ) * 100

        efficiency = co2_total / (row.get("forecasted_waste_value", base_price) + 1e-6)

        return (
            round(co2_total, 2),
            round(water_total, 2),
            round(energy_total, 2),
            round(meals, 2),
            round(score, 2),
            round(efficiency, 3)
        )
    except Exception as e:
        print(f"[❌ Sustainability Error] {e} — row: {row.get('item_id', 'UNKNOWN')}")
        return (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

def enrich_sustainability(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    (
        df["co2_saved_kg"],
        df["water_saved_liters"],
        df["energy_saved_kwh"],
        df["meals_saved"],
        df["sustainability_score"],
        df["efficiency_ratio"]
    ) = zip(*df.apply(estimate_all, axis=1))
    return df

# --- CLI TEST ---
if __name__ == "__main__":
    from services.loader import load_inventory
    df = load_inventory()
    enriched_df = enrich_sustainability(df)
    print("\n🌍 Sustainability Intelligence:")
    print(enriched_df[[
        "item_id", "item_name", "category", "forecasted_waste_units",
        "co2_saved_kg", "water_saved_liters", "energy_saved_kwh",
        "meals_saved", "sustainability_score", "efficiency_ratio"
    ]].head())
    print("\n📊 Sustainability Summary:")
    print(f"Total CO2 Saved: {enriched_df['co2_saved_kg'].sum()} kg")
    print(f"Total Water Saved: {enriched_df['water_saved_liters'].sum()} liters")
    print(f"Total Energy Saved: {enriched_df['energy_saved_kwh'].sum()} kWh")
    print(f"Total Meals Saved: {enriched_df['meals_saved'].sum()} meals")
    print(f"Average Sustainability Score: {enriched_df['sustainability_score'].mean():.2f}")
    print(f"Average Efficiency Ratio: {enriched_df['efficiency_ratio'].mean():.3f}")        
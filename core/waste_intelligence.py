import pandas as pd


def calculate_risk_score(row) -> float:
    """
    Composite score based on:
    - Time urgency (days_remaining / shelf_life_days)
    - Overstock (high stock + low daily_sales)
    - Carbon score (env. penalty of waste)
    - Perishability (elasticity + low price effect)
    """
    if row['shelf_life_days'] == 0:
        return 0.0

    urgency = 1 - (row['days_remaining'] / row['shelf_life_days'])
    overstock_ratio = min(row['current_stock'] / max(row['daily_sales'], 1), 10)
    overstock_factor = min(overstock_ratio / 5, 1.0)
    carbon_factor = row.get('carbon_score', 0) / 5
    elasticity_penalty = max(0, 1 - row.get('elasticity', 0.5))

    score = 100 * (
        0.4 * urgency +
        0.3 * overstock_factor +
        0.2 * carbon_factor +
        0.1 * elasticity_penalty
    )
    return round(min(score, 100), 2)


def tag_risk(score: float) -> str:
    if score > 75:
        return "🔴 HIGH RISK – Act Now"
    elif score > 45:
        return "🟠 MEDIUM RISK – Monitor"
    else:
        return "🟢 LOW RISK – Stable"


def forecast_spoilage(row) -> tuple[int, float]:
    days_left = row['days_remaining']
    daily_sales = max(row['daily_sales'], 1)
    projected_sales = min(row['current_stock'], daily_sales * days_left)
    expected_waste = max(row['current_stock'] - projected_sales, 0)
    waste_value = expected_waste * row['base_price']
    return int(expected_waste), round(waste_value, 2)


def recommend_action(row) -> str:
    risk = row['risk_score']
    spoilage_val = row['forecasted_waste_value']
    days = row['days_remaining']

    if days <= 1 and spoilage_val > 200:
        return "DONATE"
    elif risk > 80:
        return "Strategic Discount - Tier 1"
    elif 60 < risk <= 80:
        return "Strategic Discount - Tier 2"
    elif spoilage_val > 100:
        return "RETURN to Supplier"
    else:
        return "NO ACTION"


def enrich_inventory(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df['risk_score'] = df.apply(calculate_risk_score, axis=1)
    df['risk_tag'] = df['risk_score'].apply(tag_risk)

    spoilage = df.apply(forecast_spoilage, axis=1)
    df['forecasted_waste_units'] = [x[0] for x in spoilage]
    df['forecasted_waste_value'] = [x[1] for x in spoilage]

    df['recommended_action'] = df.apply(lambda row: recommend_action({
        'risk_score': row['risk_score'],
        'forecasted_waste_value': row['forecasted_waste_value'],
        'days_remaining': row['days_remaining']
    }), axis=1)

    return df


# === CLI TEST ===
if __name__ == "__main__":
    from services.loader import load_inventory

    df = load_inventory()
    enriched = enrich_inventory(df)
    print("\n📦 Waste Intelligence Preview:")
    print(enriched[[
        "item_id", "item_name", "current_stock",
        "risk_score", "risk_tag", "forecasted_waste_units",
        "forecasted_waste_value", "recommended_action"
    ]].head())

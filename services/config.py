from pathlib import Path

# File Paths
INVENTORY_PARQUET = Path("data/inventory.parquet")
INVENTORY_CSV = Path("data/inventory.csv")
ACTION_LOG_CSV = Path("data/action_log.csv")
ACTION_LOG_PARQUET = Path("data/actions_log.parquet")

# Spoilage Risk Thresholds
HIGH_RISK_THRESHOLD = 75
MEDIUM_RISK_THRESHOLD = 45

# Dynamic Pricing Logic
MAX_DISCOUNT = 0.5  # Max 50% off
MIN_DISCOUNT_URGENCY = 0.3  # If <30% shelf-life remains

# Restock Simulation
DELIVERY_DELAY_OPTIONS = [0, 1, 2]  # Simulate delays in days

# Sustainability Constants
CARBON_NORMALIZER = 5  # For scaling carbon impact
MEAL_WEIGHT_KG = 0.4  # Avg weight of a meal
WATER_SAVED_PER_MEAL_LITERS = 350  # Liters saved per meal diverted

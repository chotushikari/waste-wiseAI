# import pandas as pd
# from tqdm import tqdm
# from services.loader import load_inventory, save_inventory, log_action
# from core.waste_intelligence import enrich_inventory
# from core.sustainability import enrich_sustainability
# from core.decision_engine import run_decision_engine

# def simulate_day():
#     """
#     Simulate 1 day of inventory behavior.
#     - Decrease days_remaining
#     - Handle spoilage and calculate waste impact
#     - Simulate daily sales using price elasticity
#     - Dynamically update pricing
#     - Trigger restocks if due
#     - Log all actions
#     - Track carbon footprint impact
#     - Enrich with waste intelligence and sustainability metrics
#     """
#     df = load_inventory()

#     for idx, row in tqdm(df.iterrows(), total=len(df)):
#         sku = row['item_id']
#         name = row['item_name']
#         base_price = row['base_price']
#         current_price = row['dynamic_price']
#         current_stock = row['current_stock']
#         days_remaining = row['days_remaining']
#         shelf_life = row['shelf_life_days']
#         elasticity = row.get('elasticity', 0.0)
#         carbon_score = row.get('carbon_score', 0.0)

#         # --- 1. Reduce Shelf Life
#         new_days_remaining = max(0, days_remaining - 1)
#         df.at[idx, 'days_remaining'] = new_days_remaining

#         # --- 2. Spoilage Handling
#         if new_days_remaining == 0 and current_stock > 0:
#             waste_qty = current_stock
#             waste_value = waste_qty * base_price
#             carbon_impact = waste_qty * carbon_score

#             df.at[idx, 'current_stock'] = 0
#             log_action(sku, 'spoilage', waste_qty, 'Expired – Auto Spoil', waste_value)

#         # --- 3. Dynamic Pricing Logic
#         urgency = new_days_remaining / shelf_life if shelf_life > 0 else 1
#         if urgency <= 0.3 and current_stock > 0:
#             discount_factor = 1 - min(0.5, 0.1 + (0.3 - urgency))
#             new_price = round(base_price * discount_factor, 2)
#         else:
#             new_price = base_price
#         df.at[idx, 'dynamic_price'] = new_price

#         # --- 4. Sales Simulation with Price Elasticity
#         price_change_ratio = (base_price - new_price) / base_price if base_price > 0 else 0
#         adjusted_demand = row['predicted_daily_sales'] * (1 + elasticity * price_change_ratio)
#         simulated_sales = min(int(adjusted_demand), df.at[idx, 'current_stock'])
#         df.at[idx, 'current_stock'] -= simulated_sales

#         if simulated_sales > 0:
#             log_action(sku, 'sale', simulated_sales, 'Elasticity-based Sale Simulation')

#         # --- 5. Restocking Logic
#         if row['days_until_restock'] == 0:
#             restock_amount = row['initial_stock']
#             df.at[idx, 'current_stock'] += restock_amount
#             df.at[idx, 'days_until_restock'] = row['restock_frequency_days']
#             log_action(sku, 'restock', restock_amount, 'Scheduled Restock')
#         else:
#             df.at[idx, 'days_until_restock'] = max(0, row['days_until_restock'] - 1)

#     # === After Loop: Enrich & Run Decision Engine ===
#     df = enrich_inventory(df)
#     df = enrich_sustainability(df)
#     df, summary = run_decision_engine(save=False)

#     # Save state
#     save_inventory(df)

#     return df, summary


# if __name__ == "__main__":
#     df, summary = simulate_day()
#     print("\n✅ Simulated 1 full day of inventory dynamics.")
#     print(df.head())
#     print("\n📊 Daily Summary:")
#     for k, v in summary.items():
#         print(f"{k}: {v}")
# import pandas as pd
# import numpy as np
# import time
# import sys
# import io
# from datetime import datetime
# from services.loader import load_inventory, save_inventory, load_action_log
# from services.logger import batch_log_action, flush_logs_to_file
# from core.waste_intelligence import enrich_inventory
# from core.sustainability import enrich_sustainability
# from core.decision_engine import generate_daily_decisions, summarize_decisions

# # Redirect stdout to handle unicode in terminals (Windows-safe)
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# def simulate_day():
#     start_time = time.time()
#     print("\n⚙️ Starting simulation...")

#     df = load_inventory()
#     print("✅ Loaded inventory:", df.shape)

#     # === 1. Reduce Shelf Life ===
#     df['days_remaining'] = np.maximum(df['days_remaining'] - 1, 0)
#     print("✅ Updated shelf life")

#     # === 2. Spoilage Handling ===
#     expired_mask = (df['days_remaining'] <= 0) & (df['current_stock'] > 0)
#     if expired_mask.any():
#         print(f"✅ Spoilage triggered for {expired_mask.sum()} items")
#         spoilage_df = df[expired_mask].copy()
#         df.loc[expired_mask, 'current_stock'] = 0
#         spoilage_logs = pd.DataFrame({
#             "item_id": spoilage_df['item_id'],
#             "action_type": "spoilage",
#             "quantity": spoilage_df['current_stock'],
#             "reason": "Expired – Auto Spoil",
#             "value": (spoilage_df['current_stock'] * spoilage_df['base_price']).round(2)
#         }).to_dict(orient="records")
#         batch_log_action(spoilage_logs)
#     else:
#         print("✅ No spoilage triggered")

#     # === 3. Dynamic Pricing ===
#     urgency = df['days_remaining'] / df['shelf_life_days'].replace(0, 1)
#     discount = 1 - np.minimum(0.5, 0.1 + (0.3 - np.clip(urgency, None, 0.3)))
#     df['dynamic_price'] = np.where(
#         (urgency <= 0.3) & (df['current_stock'] > 0),
#         (df['base_price'] * discount).round(2),
#         df['base_price']
#     )

#     # === 4. Sales Simulation ===
#     price_diff = (df['base_price'] - df['dynamic_price']) / df['base_price'].replace(0, 1)
#     adj_demand = (df['predicted_daily_sales'] * (1 + df['elasticity'] * price_diff)).fillna(0).astype(int)
#     simulated_sales = np.minimum(adj_demand, df['current_stock'])
#     df['current_stock'] -= simulated_sales
#     sales_mask = simulated_sales > 0
#     if sales_mask.any():
#         sale_logs = pd.DataFrame({
#             "item_id": df.loc[sales_mask, 'item_id'],
#             "action_type": "sale",
#             "quantity": simulated_sales[sales_mask],
#             "reason": "Elasticity-based Sale Simulation",
#             "value": (simulated_sales[sales_mask] * df.loc[sales_mask, 'dynamic_price']).round(2)
#         }).to_dict(orient="records")
#         batch_log_action(sale_logs)

#     # === 5. Restocking ===
#     restock_mask = df['days_until_restock'] == 0
#     if restock_mask.any():
#         df.loc[restock_mask, 'current_stock'] += df.loc[restock_mask, 'initial_stock']
#         restock_logs = pd.DataFrame({
#             "item_id": df.loc[restock_mask, 'item_id'],
#             "action_type": "restock",
#             "quantity": df.loc[restock_mask, 'initial_stock'],
#             "reason": "Scheduled Restock",
#             "value": 0.0
#         }).to_dict(orient="records")
#         batch_log_action(restock_logs)
#     df['days_until_restock'] = np.where(
#         restock_mask,
#         df['restock_frequency_days'],
#         df['days_until_restock'] - 1
#     )

#     # === 6. Enrichments ===
#     df = enrich_inventory(df)
#     print("✅ Enriched waste intelligence")

#     df = enrich_sustainability(df)
#     print("✅ Enriched sustainability intelligence")

#     df = generate_daily_decisions(df)
#     print("✅ Generated daily AI decisions")

#     summary = summarize_decisions(df)

#     # === 7. Save inventory + logs ===
#     save_inventory(df)
#     print("✅ Inventory saved to Parquet")

#     flush_logs_to_file()

#     try:
#         log_df = load_action_log()
#         print(f"✅ Action logs written: {len(log_df)} total entries")
#     except Exception as e:
#         print(f"❌ Error reading action logs: {e}")

#     print("\n📊 Summary Snapshot:")
#     for k, v in summary.items():
#         print(f"  - {k}: {v}")

#     total_time = round(time.time() - start_time, 2)
#     print(f"⏱️ Total Time Taken: {total_time} seconds")

#     return df, summary


# # === CLI RUN ===
# if __name__ == "__main__":
#     updated_df, summary = simulate_day()

#     # Load today's logs
#     try:
#         logs = load_action_log()
#         logs['timestamp'] = pd.to_datetime(logs['timestamp'], errors='coerce')
#         today = datetime.now().date()
#         today_logs = logs[logs['timestamp'].dt.date == today]
#         print(f"\n🕒 Total Logs Today: {len(today_logs)}")
#         print(today_logs.tail(5))
#     except Exception as e:
#         print(f"❌ Error loading logs for today: {e}")

#     print("\n🧠 Simulated 1 day — Preview:")
#     print(updated_df.head().to_string())


# import pandas as pd
# import numpy as np
# import time
# import sys
# import io
# import argparse
# from datetime import datetime, timedelta
# from services.loader import load_inventory, save_inventory, load_action_log
# from services.logger import batch_log_action, flush_logs_to_file
# from core.waste_intelligence import enrich_inventory
# from core.sustainability import enrich_sustainability
# from core.decision_engine import generate_daily_decisions, summarize_decisions

# # Redirect stdout to handle unicode in terminals (Windows-safe)
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# def simulate_day():
#     start_time = time.time()
#     print("\n⚙️ Starting simulation...")

#     df = load_inventory()
#     print("✅ Loaded inventory:", df.shape)

#     # === 1. Reduce Shelf Life ===
#     df['days_remaining'] = np.maximum(df['days_remaining'] - 1, 0)
#     print("✅ Updated shelf life")

#     # === 2. Spoilage Handling ===
#     expired_mask = (df['days_remaining'] <= 0) & (df['current_stock'] > 0)
#     if expired_mask.any():
#         print(f"✅ Spoilage triggered for {expired_mask.sum()} items")
#         spoilage_df = df[expired_mask].copy()
#         df.loc[expired_mask, 'current_stock'] = 0
#         spoilage_logs = pd.DataFrame({
#             "item_id": spoilage_df['item_id'],
#             "action_type": "spoilage",
#             "quantity": spoilage_df['current_stock'],
#             "reason": "Expired – Auto Spoil",
#             "value": (spoilage_df['current_stock'] * spoilage_df['base_price']).round(2)
#         }).to_dict(orient="records")
#         batch_log_action(spoilage_logs)
#     else:
#         print("✅ No spoilage triggered")

#     # === 3. Dynamic Pricing ===
#     urgency = df['days_remaining'] / df['shelf_life_days'].replace(0, 1)
#     discount = 1 - np.minimum(0.5, 0.1 + (0.3 - np.clip(urgency, None, 0.3)))
#     df['dynamic_price'] = np.where(
#         (urgency <= 0.3) & (df['current_stock'] > 0),
#         (df['base_price'] * discount).round(2),
#         df['base_price']
#     )

#     # === 4. Sales Simulation ===
#     price_diff = (df['base_price'] - df['dynamic_price']) / df['base_price'].replace(0, 1)
#     adj_demand = (df['predicted_daily_sales'] * (1 + df['elasticity'] * price_diff)).fillna(0).astype(int)
#     simulated_sales = np.minimum(adj_demand, df['current_stock'])
#     df['current_stock'] -= simulated_sales
#     sales_mask = simulated_sales > 0
#     if sales_mask.any():
#         sale_logs = pd.DataFrame({
#             "item_id": df.loc[sales_mask, 'item_id'],
#             "action_type": "sale",
#             "quantity": simulated_sales[sales_mask],
#             "reason": "Elasticity-based Sale Simulation",
#             "value": (simulated_sales[sales_mask] * df.loc[sales_mask, 'dynamic_price']).round(2)
#         }).to_dict(orient="records")
#         batch_log_action(sale_logs)

#     # === 5. Restocking ===
#     restock_mask = df['days_until_restock'] == 0
#     if restock_mask.any():
#         df.loc[restock_mask, 'current_stock'] += df.loc[restock_mask, 'initial_stock']
#         restock_logs = pd.DataFrame({
#             "item_id": df.loc[restock_mask, 'item_id'],
#             "action_type": "restock",
#             "quantity": df.loc[restock_mask, 'initial_stock'],
#             "reason": "Scheduled Restock",
#             "value": 0.0
#         }).to_dict(orient="records")
#         batch_log_action(restock_logs)
#     df['days_until_restock'] = np.where(
#         restock_mask,
#         df['restock_frequency_days'],
#         df['days_until_restock'] - 1
#     )

#     # === 6. Enrichments ===
#     df = enrich_inventory(df)
#     print("✅ Enriched waste intelligence")

#     df = enrich_sustainability(df)
#     print("✅ Enriched sustainability intelligence")

#     df = generate_daily_decisions(df)
#     print("✅ Generated daily AI decisions")

#     summary = summarize_decisions(df)

#     # === 7. Save inventory + logs ===
#     save_inventory(df)
#     print("✅ Inventory saved to Parquet")

#     flush_logs_to_file()

#     try:
#         log_df = load_action_log()
#         print(f"✅ Action logs written: {len(log_df)} total entries")
#     except Exception as e:
#         print(f"❌ Error reading action logs: {e}")

#     print("\n📊 Summary Snapshot:")
#     for k, v in summary.items():
#         print(f"  - {k}: {v}")

#     total_time = round(time.time() - start_time, 2)
#     print(f"⏱️ Total Time Taken: {total_time} seconds")

#     return df, summary

# def simulate_n_days(n):
#     print(f"\n📆 Simulating for {n} day(s)...")
#     for day in range(1, n+1):
#         print(f"\n🔁 Day {day}:")
#         simulate_day()

# # === CLI RUN ===


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--days", type=int, default=1, help="Simulate for N days")
#     parser.add_argument("--weeks", type=int, help="Simulate for N weeks")
#     parser.add_argument("--months", type=int, help="Simulate for N months")
#     args = parser.parse_args()

#     total_days = args.days
#     if args.weeks:
#         total_days = args.weeks * 7
#     if args.months:
#         total_days = args.months * 30

#     print(f"\n📆 Simulating for {total_days} day(s)...\n")
#     for day in range(total_days):
#         print(f"\n🔁 Day {day + 1}:")
#         simulate_day()

import pandas as pd
import numpy as np
import time
import logging
from datetime import datetime, timedelta
import sys
import io
import argparse
import random

from services.loader import load_inventory, save_inventory
from services.logger import batch_log_action, flush_logs_to_file, log_full_action_context
from core.waste_intelligence import enrich_inventory
from core.sustainability import enrich_sustainability
from core.decision_engine import generate_daily_decisions, summarize_decisions
from services.persistence import save_dual, save_sustainability_log

# === Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # Unicode fix

# === Global config
IMPORTANT_ACTIONS = {
    "DONATE", "RETURN to Supplier", "Strategic Discount - Tier 1", "Strategic Discount - Tier 2"
}
current_date = datetime.now().date()


# === ACTION LOG HELPERS ===

def log_spoilage(df, mask, verbose=True):
    spoilage_df = df[mask].copy()
    df.loc[mask, 'current_stock'] = 0
    logs = pd.DataFrame({
        "item_id": spoilage_df['item_id'],
        "action_type": "spoilage",
        "quantity": spoilage_df['current_stock'],
        "reason": "Expired – Auto Spoil",
        "value": (spoilage_df['current_stock'] * spoilage_df['base_price']).round(2)
    }).to_dict(orient="records")
    batch_log_action(logs)
    if verbose:
        logger.info(f"☠️ Spoilage: {mask.sum()} items expired")


def log_sales(sales_data):
    if not sales_data:
        return
    logs = pd.DataFrame({
        "item_id": [s['item_id'] for s in sales_data],
        "action_type": "sale",
        "quantity": [s['quantity'] for s in sales_data],
        "reason": "Elasticity-based Sale Simulation",
        "value": [round(s['quantity'] * s['price'], 2) for s in sales_data]
    }).to_dict(orient="records")
    batch_log_action(logs)


def log_restock(df, mask, verbose=True):
    df.loc[mask, 'current_stock'] += df.loc[mask, 'initial_stock']
    logs = pd.DataFrame({
        "item_id": df.loc[mask, 'item_id'],
        "action_type": "restock",
        "quantity": df.loc[mask, 'initial_stock'],
        "reason": "Scheduled Restock",
        "value": 0.0
    }).to_dict(orient="records")
    batch_log_action(logs)
    if verbose:
        logger.info(f"📦 Restocked: {mask.sum()} items")


# === DAILY SIMULATION ===

def simulate_day(verbose=True):
    global current_date
    if verbose:
        logger.info("\n⚙️ Simulating Day")

    try:
        df = load_inventory()
        df['days_remaining'] = np.maximum(df['days_remaining'] - 1, 0)

        # === Spoilage
        spoil_mask = (df['days_remaining'] <= 0) & (df['current_stock'] > 0)
        if spoil_mask.any():
            log_spoilage(df, spoil_mask, verbose)

        # === Dynamic Pricing + Sales Simulation
        sales_data = []
        is_weekend = current_date.weekday() in [5, 6]
        multiplier = 1.2 if is_weekend else 1.0

        for idx, row in df.iterrows():
            base, elasticity, pred_sales = row['base_price'], row['elasticity'], row['predicted_daily_sales']
            stock, days_rem = row['current_stock'], row['days_remaining']
            floor = max(base - elasticity, 0.01)
            base_demand = pred_sales * multiplier

            # Price elasticity factor
            elasticity_boost = (1 - (row['dynamic_price'] - base) / base) * elasticity if base > 0 else 0
            sales = max(1, int(base_demand + random.uniform(-5, 5) + elasticity_boost * base_demand))
            sales = min(sales, stock)
            df.at[idx, 'current_stock'] -= sales

            if sales > 0:
                sales_data.append({
                    "item_id": row['item_id'],
                    "quantity": sales,
                    "price": row['dynamic_price']
                })

            # Recalculate dynamic price
            if pred_sales > 0 and days_rem > 0:
                predicted_total = pred_sales * days_rem
                stock_ratio = stock / predicted_total if predicted_total > 0 else 0
                if stock_ratio > 1.2:
                    discount = elasticity * 0.8
                    new_price = round(max(base - discount, floor), 2)
                else:
                    new_price = base
            else:
                new_price = base

            if days_rem <= 2 and stock > 0:
                new_price = round(max(new_price * 0.9, base * 0.5), 2)

            df.at[idx, 'dynamic_price'] = new_price

        log_sales(sales_data)

        # === Restocking
        restock_mask = df['days_until_restock'] <= 0
        if restock_mask.any():
            for idx in df[restock_mask].index:
                delay = random.choice([0, 1, 2])
                df.at[idx, 'days_until_restock'] = df.at[idx, 'restock_frequency_days'] + delay
        else:
            df['days_until_restock'] -= 1
        log_restock(df, restock_mask, verbose)

        # === AI Intelligence
        df = enrich_inventory(df)
        df = enrich_sustainability(df)
        df = generate_daily_decisions(df)
        save_dual(df, base_filename="inventory_updated")
        save_sustainability_log(df)

        # === Full AI Context Log (CSV + Parquet)
        log_full_action_context(df)

        # === Log Only Recommended Actions
        ai_loggable = df[df['recommended_action'].isin(IMPORTANT_ACTIONS)]
        if not ai_loggable.empty:
            logs = pd.DataFrame({
                "item_id": ai_loggable['item_id'],
                "action_type": ai_loggable['recommended_action'],
                "quantity": ai_loggable['forecasted_waste_units'].fillna(0).astype(int),
                "reason": ai_loggable['tactical_note'],
                "value": ai_loggable['forecasted_waste_value'].fillna(0).round(2)
            }).to_dict(orient="records")
            batch_log_action(logs)
            logger.info(f"🤖 AI Actions: {len(logs)} logged")
        else:
            logger.info("🤖 AI Actions: None today")

        # === Final Save & Cleanup
        save_inventory(df)
        flush_logs_to_file()
        current_date += timedelta(days=1)

        summary = summarize_decisions(df)
        return df, summary

    except Exception as e:
        logger.error(f"[❌ Simulation Error] {e}")
        raise


# === SIMULATE MULTIPLE DAYS ===

def simulate_n_days(n):
    logger.info(f"\n📅 Running {n} day(s) simulation")
    for day in range(1, n + 1):
        logger.info(f"\n🔁 Day {day}")
        start = time.time()
        try:
            df, summary = simulate_day(verbose=True)
            logger.info("📊 Daily Summary:")
            for k, v in summary.items():
                logger.info(f"   - {k}: {v}")
            logger.info(f"✅ Done in {round(time.time() - start, 2)}s")
        except Exception as e:
            logger.error(f"[❌ Day {day} Failed] {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=1, help="Number of days to simulate")
    args = parser.parse_args()
    simulate_n_days(args.days)

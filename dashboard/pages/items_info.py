import streamlit as st
import pandas as pd

# --- Config ---
st.set_page_config(page_title="Item Info | Walmart AI", layout="wide")

# --- Custom Styling to match dashboard with better visibility ---
def set_custom_styles():
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3 {
            color: #002244 !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }
        .info-card {
            background-color: #e9f1f7;
            padding: 1.2rem 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }
        .info-title {
            font-size: 15px;
            font-weight: 600;
            color: #1d3557;
            margin-top: 10px;
            margin-bottom: 2px;
        }
        .info-value {
            font-size: 19px;
            font-weight: 600;
            color: #000000;
            margin-bottom: 10px;
        }
        .action-log {
            background-color: #dceefb;
            border-left: 4px solid #005f99;
            padding: 12px 16px;
            margin-bottom: 12px;
            border-radius: 6px;
            color: #002b4c;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)


set_custom_styles()

# --- Load Dataset ---
@st.cache_data
def load_data():
    return pd.read_csv("../data/inventory.csv", parse_dates=["last_restock_date", "next_restock_date"])

df = load_data()

# --- Retrieve Item from State ---
if "selected_item_id" not in st.session_state:
    st.error("No item selected. Please go back to the dashboard.")
    st.stop()

item_id = st.session_state.selected_item_id
item = df[df["item_id"] == item_id].iloc[0]

# --- Page Title ---
st.markdown(f"<h1>Item Info: {item['item_name']}</h1>", unsafe_allow_html=True)

# --- Layout: Left Info + Right Action Log ---
col1, col2 = st.columns([3, 1], gap="large")

# ------------------------- LEFT COLUMN ------------------------
with col1:
    st.subheader("Overview")

    with st.container():
        st.markdown(f"""
        <div class="info-card">
            <div class="info-title">Category</div><div class="info-value">{item['category']}</div>
            <div class="info-title">Department</div><div class="info-value">{item['department']}</div>
            <div class="info-title">Shelf Life (days)</div><div class="info-value">{item['shelf_life_days']}</div>
            <div class="info-title">Current Stock</div><div class="info-value">{item['current_stock']}</div>
            <div class="info-title">Dynamic Price</div><div class="info-value">₹{item['dynamic_price']}</div>
            <div class="info-title">Risk Tag</div><div class="info-value">{item['risk_tag']}</div>
            <div class="info-title">Sustainability Score</div><div class="info-value">{item['sustainability_score']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Sustainability Impact")
    with st.container():
        st.markdown(f"""
        <div class="info-card">
            <div class="info-title">CO₂ Saved</div><div class="info-value">{item['co2_saved_kg']} kg</div>
            <div class="info-title">Water Saved</div><div class="info-value">{item['water_saved_liters']} L</div>
            <div class="info-title">Energy Saved</div><div class="info-value">{item['energy_saved_kwh']} kWh</div>
            <div class="info-title">Meals Saved</div><div class="info-value">{item['meals_saved']}</div>
        </div>
        """, unsafe_allow_html=True)

# ------------------------- RIGHT COLUMN ------------------------
with col2:
    st.subheader("Action Logs")

    logs = []
    if item["recommended_action"]:
        logs.append(f"Recommended Action: {item['recommended_action']}")
    if not pd.isna(item["last_restock_date"]):
        logs.append(f"Restocked on {item['last_restock_date'].date()}")
    if not pd.isna(item["next_restock_date"]):
        logs.append(f"Next Restock: {item['next_restock_date'].date()}")
    if item["risk_tag"] == "High":
        logs.append(f"Risk: High")

    for log in logs:
        st.markdown(f'<div class="action-log">{log}</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Back to Dashboard"):
        del st.session_state.selected_item_id
        st.switch_page("app.py")

# import streamlit as st
# import pandas as pd
# import datetime

# # ----- Page Config -----
# st.set_page_config(page_title="Walmart Inventory Dashboard", layout="wide")

# # ----- Bright, Clear Styling -----
# def set_custom_styles():
#     st.markdown("""
#         <style>
#         .stApp {
#             background-color: #ffffff;
#             color: #000000;
#             font-family: 'Segoe UI', sans-serif;
#         }
#         h1, h2, h3, h4 {
#             color: #003366;
#             font-weight: 700;
#         }
#         .block-container {
#             padding-top: 2rem;
#         }
#         .metric-box {
#             background-color: #f0f4f8;
#             padding: 1rem;
#             border-radius: 10px;
#             box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
#             text-align: center;
#         }
#         .metric-label {
#             font-size: 16px;
#             color: #333333;
#         }
#         .metric-value {
#             font-size: 28px;
#             font-weight: bold;
#             color: #0077b6;
#         }
#         .dataframe th, .dataframe td {
#             font-size: 14px !important;
#             padding: 8px !important;
#         }
#         .dataframe tbody tr:hover {
#             background-color: #eaf4ff !important;
#         }
#         footer {
#             visibility: hidden;
#         }
#         </style>
#     """, unsafe_allow_html=True)

# set_custom_styles()

# # ----- Title -----
# st.markdown("<h1>Walmart Inventory Dashboard</h1>", unsafe_allow_html=True)

# # ----- Load Dataset -----
# @st.cache_data
# def load_data():
#     return pd.read_csv("../data/inventory.csv", parse_dates=["last_restock_date", "next_restock_date"])

# df = load_data()

# # ----- Filters -----
# st.subheader("Inventory Filters")

# with st.container():
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.markdown("**Category**")
#         category_filter = st.multiselect(
#             label="",
#             options=df["category"].unique(),
#             placeholder="Select one or more categories"
#         )

#     with col2:
#         st.markdown("**Department**")
#         dept_filter = st.multiselect(
#             label="",
#             options=df["department"].unique(),
#             placeholder="Select one or more departments"
#         )

#     with col3:
#         st.markdown("**Item Name Search**")
#         search_query = st.text_input(
#             label="",
#             placeholder="Type item name..."
#         )


# # ----- Date Filter -----
# if "date" in df.columns:
#     st.subheader("Date Filter")
#     date_range = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days"])
#     today = datetime.date.today()
#     cutoff = today - datetime.timedelta(days=7 if "7" in date_range else 30)
#     df = df[df["date"] >= pd.to_datetime(cutoff)]

# # ----- Apply Filters -----
# if category_filter:
#     df = df[df["category"].isin(category_filter)]
# if dept_filter:
#     df = df[df["department"].isin(dept_filter)]
# if search_query:
#     df = df[df["item_name"].str.contains(search_query, case=False)]

# # ----- KPIs -----
# st.subheader("Key Performance Indicators")
# kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# with kpi1:
#     st.markdown('<div class="metric-box"><div class="metric-label">Total Items</div><div class="metric-value">%s</div></div>' %
#                 df.shape[0], unsafe_allow_html=True)

# with kpi2:
#     st.markdown('<div class="metric-box"><div class="metric-label">Items Donated</div><div class="metric-value">%s</div></div>' %
#                 df[df["current_stock"] == 0].shape[0], unsafe_allow_html=True)

# with kpi3:
#     st.markdown('<div class="metric-box"><div class="metric-label">Avg. Predicted Demand</div><div class="metric-value">%.2f</div></div>' %
#                 df["predicted_daily_sales"].mean(), unsafe_allow_html=True)

# with kpi4:
#     st.markdown('<div class="metric-box"><div class="metric-label">Avg. Carbon Score</div><div class="metric-value">%.2f</div></div>' %
#                 df["carbon_score"].mean(), unsafe_allow_html=True)

# # ----- Inventory Table with Clickable Item Names -----
# st.subheader("Filtered Inventory Table")

# # Just the columns we need
# display_df = df[["item_id", "item_name", "category", "department", "recommended_action"]].reset_index(drop=True)

# # Headers
# st.markdown("""
# <style>
# .custom-table {
#     border-collapse: collapse;
#     width: 100%;
# }
# .custom-table th, .custom-table td {
#     text-align: left;
#     padding: 8px;
#     font-size: 15px;
#     border-bottom: 1px solid #ddd;
# }
# .custom-table tr:hover {
#     background-color: #f1f1f1;
# }
# .custom-button {
#     background-color: #0077b6;
#     color: white;
#     border: none;
#     padding: 6px 12px;
#     border-radius: 4px;
#     cursor: pointer;
# }
# </style>
# """, unsafe_allow_html=True)

# # Render each row
# for i, row in display_df.iterrows():
#     cols = st.columns([3, 2, 2, 3])

#     with cols[0]:
#         if st.button(row["item_name"], key=f"btn_{row['item_id']}"):
#             st.session_state.selected_item_id = row["item_id"]
#             st.switch_page("pages/items_info.py")

#     cols[1].write(row["category"])
#     cols[2].write(row["department"])
#     cols[3].write(row["recommended_action"])


import streamlit as st
import pandas as pd
import datetime

# ----- Page Config -----
st.set_page_config(page_title="Walmart Inventory Dashboard", layout="wide")

# ----- Custom Styling -----
def set_custom_styles():
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: #000000;
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h2, h3, h4 {
            color: #003366;
            font-weight: 700;
        }

        .block-container {
            padding-top: 2rem;
        }

        .metric-box {
            background-color: #f0f4f8;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        .metric-label {
            font-size: 16px;
            color: #333333;
        }

        .metric-value {
            font-size: 28px;
            font-weight: bold;
            color: #0077b6;
        }

        .dataframe th, .dataframe td {
            font-size: 14px !important;
            padding: 8px !important;
        }

        .dataframe tbody tr:hover {
            background-color: #eaf4ff !important;
        }

        .stButton>button {
            background-color: transparent !important;
            color: #003366 !important;
            border: none !important;
            text-align: left !important;
            font-weight: 600;
            font-size: 16px;
            padding: 0 !important;
            margin: 0 !important;
        }

        .stButton>button:hover {
            text-decoration: underline;
            color: #0077b6 !important;
            cursor: pointer;
        }

        /* ---- Radio Button Styling ---- */
        .stRadio > div {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .stRadio label {
            background-color: #f0f4f8;
            border-radius: 8px;
            padding: 6px 12px;
            font-weight: 600;
            color: #003366;
            cursor: pointer;
        }

        .stRadio div[role="radiogroup"] > label[data-selected="true"] {
            background-color: #0077b6;
            color: white !important;
        }

        footer {
            visibility: hidden;
        }
        </style>
    """, unsafe_allow_html=True)


set_custom_styles()

# ----- Title -----
st.markdown("<h1>Walmart Inventory Dashboard</h1>", unsafe_allow_html=True)

# ----- Load Dataset -----
@st.cache_data
def load_data():
    return pd.read_csv("../data/inventory.csv", parse_dates=["last_restock_date", "next_restock_date"])

df = load_data()

# ----- Filters -----
st.subheader("Inventory Filters")

with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Category**")
        category_filter = st.multiselect(
            label="",
            options=df["category"].dropna().unique(),
            placeholder="Select one or more categories"
        )

    with col2:
        st.markdown("**Department**")
        dept_filter = st.multiselect(
            label="",
            options=df["department"].dropna().unique(),
            placeholder="Select one or more departments"
        )

    with col3:
        st.markdown("**Item Name Search**")
        search_query = st.text_input(
            label="",
            placeholder="Type item name..."
        )

# ----- Date Filter -----
if "last_restock_date" in df.columns:
    st.subheader("Date Filter")
    date_range = st.selectbox("Time Period", ["Last 30 Days", "Last 7 Days", "Today"])
    today = datetime.date.today()
    if "30" in date_range:
        cutoff = today - datetime.timedelta(days=30)
    elif "7" in date_range:
        cutoff = today - datetime.timedelta(days=7)
    else:
        cutoff = today
    df = df[df["last_restock_date"] >= pd.to_datetime(cutoff)]

# ----- Apply Filters -----
if category_filter:
    df = df[df["category"].isin(category_filter)]
if dept_filter:
    df = df[df["department"].isin(dept_filter)]
if search_query:
    df = df[df["item_name"].str.contains(search_query, case=False)]

# ----- KPIs -----
st.subheader("Key Performance Indicators")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f'<div class="metric-box"><div class="metric-label">Total Items</div><div class="metric-value">{df.shape[0]}</div></div>', unsafe_allow_html=True)

with kpi2:
    items_donated = df[df["current_stock"] == 0].shape[0]
    st.markdown(f'<div class="metric-box"><div class="metric-label">Items Donated</div><div class="metric-value">{items_donated}</div></div>', unsafe_allow_html=True)

with kpi3:
    total_daily_sales = int(df["daily_sales"].sum()) if "daily_sales" in df.columns else 0
    st.markdown(f'<div class="metric-box"><div class="metric-label">Total Sales</div><div class="metric-value">{total_daily_sales}</div></div>', unsafe_allow_html=True)

with kpi4:
    latest_restock = df["next_restock_date"].max().date() if "next_restock_date" in df.columns else "N/A"
    st.markdown(f'<div class="metric-box"><div class="metric-label">Next Restock (Latest)</div><div class="metric-value">{latest_restock}</div></div>', unsafe_allow_html=True)

# ----- Inventory Table Price Toggle -----
st.subheader("Filtered Inventory Table")

# Price Toggle
price_toggle = st.radio("Select Price Type", ["Base Price", "Dynamic Price"], horizontal=True)
price_column = "base_price" if price_toggle == "Base Price" else "dynamic_price"

# Check if DataFrame is empty
if df.empty:
    st.warning("No inventory items match your filters.")
else:
    # ----- Column Headers -----
    header_cols = st.columns([3, 2, 2, 2])
    header_labels = ["Item Name", "Category", "Department", price_toggle]
    for col, label in zip(header_cols, header_labels):
        col.markdown(f"**{label}**")

    # ----- Inventory Rows -----
    for i, row in df.iterrows():
        cols = st.columns([3, 2, 2, 2])

        with cols[0]:
            if st.button(row["item_name"], key=f"btn_{row['item_id']}"):
                st.session_state.selected_item_id = row["item_id"]
                st.switch_page("pages/items_info.py")

        cols[1].write(row["category"])
        cols[2].write(row["department"])
        price = row[price_column]
        cols[3].write(f"${price:.2f}" if pd.notnull(price) else "N/A")

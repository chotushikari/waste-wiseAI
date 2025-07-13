import streamlit as st

# ----- Page Configuration -----
st.set_page_config(page_title="Walmart Sustainability Dashboard", layout="wide")

# ----- Custom Styling -----
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        padding: 2rem;
    }

    h1 {
        color: #003366;
        font-weight: 700;
    }

    h4 {
        color: #003366;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }

    .explore-section h3 {
        color: #003366;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    .explore-section ul {
        list-style-type: none;
        padding-left: 1rem;
    }

    .explore-section li {
        font-size: 16px;
        color: #003366;
        padding: 0.4rem 0;
        font-weight: 500;
    }

    .explore-section li::before {
        content: "• ";
        color: #0077b6;
        font-weight: bold;
        margin-right: 6px;
    }

    hr {
        border: 0;
        height: 1px;
        background: #e1e1e1;
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ----- Header -----
st.markdown("""
    <h1 style='color:#003366; font-weight:700;'>🌿 Walmart AI-Powered Sustainability Dashboard</h1>
    <h4 style='color:#003366; font-weight:500;'>Use the sidebar to explore insights on inventory, sustainability efforts, and item-level analysis.</h4>
    <hr>
""", unsafe_allow_html=True)

# ----- Welcome Message -----
st.markdown("""
<div class='explore-section'>
    <h3>🏁 Start exploring:</h3>
    <ul>
        <li>📊 Go to the <strong>Dashboard</strong> page to view filters, KPIs, and suggestions</li>
        <li>🌱 Visit the <strong>Sustainability</strong> page to track impact</li>
        <li>📋 Check the <strong>Items Info</strong> page for item-specific details</li>
    </ul>
</div>
""", unsafe_allow_html=True)

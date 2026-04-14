import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import joblib

from src.price_optimizer import optimize_price
from src.simulation import compare_prices

st.set_page_config(page_title="Dynamic Price Optimizer", layout="wide")

st.title("💰 Dynamic Price Optimization System")
st.write("Optimize product pricing using Machine Learning")


# Load model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "models", "xgb_model.pkl")

model = joblib.load(model_path)

# Feature names (VERY IMPORTANT)
feature_names = [
    'Store', 'DayOfWeek', 'Promo', 'SchoolHoliday',
    'CompetitionDistance', 'CompetitionDuration',
    'PromoDuration', 'Month', 'Price',
    'StoreType_b', 'StoreType_c', 'StoreType_d',
    'Assortment_b', 'Assortment_c'
]


st.subheader("📥 Enter Business Context")

# ---------- Demand Factors ----------
st.markdown("### 📊 Demand Factors")

col1, col2, col3 = st.columns(3)

with col1:
    day_of_week = st.slider(
        "Day of Week",
        0, 6, 1,
        help="Weekends usually have higher sales"
    )

    promo = st.selectbox(
        "Promotion Running?",
        [0, 1],
        help="Promotions increase demand"
    )

with col2:
    school_holiday = st.selectbox(
        "School Holiday?",
        [0, 1],
        help="Holidays can increase store traffic"
    )

    month = st.slider(
        "Month",
        1, 12, 6,
        help="Seasonality affects demand"
    )

with col3:
    competition_distance = st.number_input(
        "Competition Distance",
        value=500.0,
        help="Closer competitors reduce sales"
    )

# ---------- Store Info ----------
st.markdown("### 🏪 Store Characteristics")

col4, col5 = st.columns(2)

with col4:
    store = st.number_input("Store ID", value=1)

    store_type = st.selectbox(
        "Store Type",
        ['a', 'b', 'c', 'd'],
        help="Different store types have different pricing power"
    )

with col5:
    assortment = st.selectbox(
        "Assortment",
        ['a', 'b', 'c'],
        help="More variety usually attracts more customers"
    )

# ---------- Pricing ----------
st.markdown("### 💰 Pricing")

price = st.slider(
    "Current Price",
    100, 1200, 400,
    help="Model will optimize around this price"
)

# converting input to model format 
input_data = {
    'Store': store,
    'DayOfWeek': day_of_week,
    'Promo': promo,
    'SchoolHoliday': school_holiday,
    'CompetitionDistance': competition_distance,
    'CompetitionDuration': 12,  # default
    'PromoDuration': 5,         # default
    'Month': month,
    'Price': price,
    'StoreType_b': 0,
    'StoreType_c': 0,
    'StoreType_d': 0,
    'Assortment_b': 0,
    'Assortment_c': 0
}

# One-hot encoding manually
if store_type == 'b':
    input_data['StoreType_b'] = 1
elif store_type == 'c':
    input_data['StoreType_c'] = 1
elif store_type == 'd':
    input_data['StoreType_d'] = 1

if assortment == 'b':
    input_data['Assortment_b'] = 1
elif assortment == 'c':
    input_data['Assortment_c'] = 1

input_df = pd.DataFrame([input_data])

st.markdown("### 🚀 Step 2: Optimize Price")

# run optimization when button is clicked
import matplotlib.pyplot as plt

if st.button("🚀 Optimize Price", use_container_width=True):

    row = input_df.iloc[0]

    best_price, best_revenue, prices, revenues = optimize_price(
        row,
        model,
        feature_names
    )
    st.divider()
    # ---------- RESULT ----------
    st.subheader("✅ Optimal Price")
    st.success(f"₹ {best_price:.2f}")

    st.subheader("💰 Expected Revenue")
    st.info(f"₹ {best_revenue:,.2f}")

    st.subheader("📈 Revenue vs Price")

    fig, ax = plt.subplots()

    ax.plot(prices, revenues)
    ax.scatter(best_price, best_revenue,s=100)  # highlight optimal
    ax.annotate("Optimal", (best_price, best_revenue))
    ax.set_xlabel("Price")
    ax.set_ylabel("Revenue")
    ax.set_title("Revenue Optimization Curve")

    st.pyplot(fig)
    
    st.success(f"📌 Revenue peaks around ₹{best_price:.0f}, which is why this price is recommended.")

   # explains why thes price?
    st.subheader("🔍 Why this price?")
    reasons = []

    if price > best_price:
      reasons.append("• Current price is higher than optimal → may reduce demand")

    elif price < best_price:
       reasons.append("• Current price is lower → opportunity to increase revenue")

    if promo == 1:
      reasons.append("• Promotion is boosting demand significantly")

    if competition_distance < 500:
     reasons.append("• Nearby competitors are limiting pricing power")

    if month in [11, 12]:
      reasons.append("• Seasonal demand is high during this period")

# Show top 3 reasons
    for r in reasons[:3]:
     st.write(r)

# confidence 
    st.subheader("📊 Confidence")

   # Determine confidence level
    if best_revenue > 1000000:
      confidence = "High"
      emoji = "🟢"
    elif best_revenue > 700000:
      confidence = "Moderate"
      emoji = "🟡"
    else:
       confidence = "Low"
       emoji = "🔴"

    

    col1, col2 = st.columns([1, 3])

    with col1:
     st.markdown(f"### {emoji} {confidence}")

    with col2:
     st.markdown(
        "<div style='margin-top: 8px; color: gray;'>Based on historical patterns</div>",
        unsafe_allow_html=True
      )
    
    
    # A/B testing for price comparison
    st.subheader("📊 Price Comparison (A/B Testing)")

    comparison = compare_prices(
        row,
        model,
        feature_names,
        prices=[300, 400]
     )

    for result in comparison:
        st.write(
            f"Price ₹{result['price']} → "
            f"Revenue: ₹{result['mean_revenue']:,.0f} | "
            f"Risk: ₹{result['risk_std']:,.0f}"
        )

    st.info("💡 Try changing inputs to see how pricing strategy adapts.")
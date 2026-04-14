import numpy as np
import pandas as pd


def optimize_price(row, model, feature_names):
    price_range = np.linspace(row['Price'] * 0.7, row['Price'] * 1.4, 30)

    best_price = None
    best_revenue = -np.inf

    prices = []
    revenues = []

    for price in price_range:
        temp = row.copy()
        temp['Price'] = price

        temp_df = pd.DataFrame([temp])

        # Ensure all columns match training
        for col in feature_names:
            if col not in temp_df.columns:
                temp_df[col] = 0

        temp_df = temp_df[feature_names]

        pred_sales = model.predict(temp_df)[0]
        pred_sales = max(pred_sales, 1)  # avoid negative/zero

        revenue = price * pred_sales

        prices.append(price)
        revenues.append(revenue)

        if revenue > best_revenue:
            best_revenue = revenue
            best_price = price

    return best_price, best_revenue, prices, revenues
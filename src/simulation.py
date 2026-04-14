import numpy as np
import pandas as pd


def simulate_revenue(row, model, feature_names, price, n_sim=100):
    """
    Simulate revenue multiple times for a given price
    Returns mean and risk (std deviation)
    """

    revenues = []

    for _ in range(n_sim):
        temp_row = row.copy()
        temp_row['Price'] = price

        temp_df = pd.DataFrame([temp_row])

        # Align with training columns
        temp_df = temp_df.reindex(columns=feature_names, fill_value=0)

        # Predict demand
        pred_sales = model.predict(temp_df)[0]

        # Add randomness (real-world uncertainty)
        noise = np.random.normal(1, 0.1)
        pred_sales = pred_sales * noise

        pred_sales = max(pred_sales, 0)

        revenue = price * pred_sales
        revenues.append(revenue)

    return {
        "price": price,
        "mean_revenue": float(round(np.mean(revenues), 2)),
        "risk_std": float(round(np.std(revenues), 2))
    }


def compare_prices(row, model, feature_names, prices=[300, 400]):
    """
    Compare multiple price points (A/B testing style)
    """

    results = []

    for price in prices:
        result = simulate_revenue(row, model, feature_names, price)
        results.append(result)

    return results
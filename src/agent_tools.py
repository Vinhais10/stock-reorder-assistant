"""
Tools that the AI agent can call.

Each tool wraps existing logic from reorder.py so the agent
never re-implements business rules - it only orchestrates them.
"""

import pandas as pd
from reorder import (
    load_sales_data,
    calculate_avg_daily_sales,
    calculate_reorder_points,
)

_cache = {}


def _get_result_df():
    """Load data once, reuse everywhere."""
    if "result" not in _cache:
        sales = load_sales_data()
        products = pd.read_csv("products.csv")
        avg = calculate_avg_daily_sales(sales)
        _cache["result"] = calculate_reorder_points(products, avg)
    return _cache["result"]


def list_products_needing_reorder():
    """Return every product whose stock is below its reorder point."""
    df = _get_result_df()
    flagged = df[df["needs_reorder"]]
    return [
        {
            "product_id": row["product_id"],
            "product_name": row["product_name"],
            "current_stock": int(row["current_stock"]),
            "reorder_point": round(float(row["reorder_point"]), 1),
            "shortage": round(float(row["reorder_point"] - row["current_stock"]), 1),
        }
        for _, row in flagged.iterrows()
    ]


def get_product_info(product_id):
    """Return full info for a single product by its ID."""
    df = _get_result_df()
    row = df[df["product_id"] == product_id]
    if row.empty:
        return {"error": f"Product '{product_id}' not found"}
    row = row.iloc[0]
    return {
        "product_id": row["product_id"],
        "product_name": row["product_name"],
        "current_stock": int(row["current_stock"]),
        "lead_time_days": int(row["lead_time_days"]),
        "safety_stock": int(row["safety_stock"]),
        "avg_daily_sales": round(float(row["avg_daily_sales"]), 2),
        "reorder_point": round(float(row["reorder_point"]), 1),
        "needs_reorder": bool(row["needs_reorder"]),
    }


def get_reorder_point(product_id):
    """Show the reorder point calculation breakdown for a product."""
    info = get_product_info(product_id)
    if "error" in info:
        return info
    formula = (
        f"({info['avg_daily_sales']} sales/day x {info['lead_time_days']} days) "
        f"+ {info['safety_stock']} safety stock = {info['reorder_point']}"
    )
    return {
        "product_id": info["product_id"],
        "formula": formula,
        "reorder_point": info["reorder_point"],
        "current_stock": info["current_stock"],
        "needs_reorder": info["needs_reorder"],
    }


def get_sales_trend(product_id, days=30):
    """Return daily sales for the last N days for a product."""
    sales = load_sales_data()
    product_sales = sales[sales["StockCode"] == product_id].copy()
    if product_sales.empty:
        return {"error": f"No sales found for '{product_id}'"}
    max_date = product_sales["InvoiceDate"].max()
    cutoff = max_date - pd.Timedelta(days=days)
    recent = product_sales[product_sales["InvoiceDate"] >= cutoff]
    daily = recent.groupby(recent["InvoiceDate"].dt.date)["Quantity"].sum()
    total = int(daily.sum())
    avg = round(float(daily.mean()), 2) if not daily.empty else 0
    return {
        "product_id": product_id,
        "period_days": days,
        "total_units_sold": total,
        "avg_daily_units": avg,
        "days_with_sales": len(daily),
        "peak_day": str(daily.idxmax()) if not daily.empty else None,
        "peak_units": int(daily.max()) if not daily.empty else 0,
    }


def simulate_scenario(product_id, new_lead_time):
    """Recalculate reorder point with a different lead time."""
    info = get_product_info(product_id)
    if "error" in info:
        return info
    new_point = (info["avg_daily_sales"] * new_lead_time) + info["safety_stock"]
    new_needs = info["current_stock"] < new_point
    return {
        "product_id": product_id,
        "current_lead_time": info["lead_time_days"],
        "new_lead_time": new_lead_time,
        "current_reorder_point": info["reorder_point"],
        "new_reorder_point": round(new_point, 1),
        "current_stock": info["current_stock"],
        "currently_flagged": info["needs_reorder"],
        "would_be_flagged": new_needs,
        "change": "no change" if new_needs == info["needs_reorder"] else "STATUS WOULD CHANGE",
    }


TOOLS = {
    "list_products_needing_reorder": list_products_needing_reorder,
    "get_product_info": get_product_info,
    "get_reorder_point": get_reorder_point,
    "get_sales_trend": get_sales_trend,
    "simulate_scenario": simulate_scenario,
}

import pandas as pd
from reorder import calculate_reorder_points

test_products = pd.DataFrame({
    'product_id': ['TEST-1'],
    'product_name': ['Test Product'],
    'lead_time_days': [10],
    'current_stock': [50],
    'safety_stock': [20]
})

test_avg_sales = pd.DataFrame({
    'product_id': ['TEST-1'],
    'avg_daily_sales': [5.0]
})

result = calculate_reorder_points(test_products, test_avg_sales)

expected_reorder_point = (5.0 * 10) + 20
assert result['reorder_point'].iloc[0] == expected_reorder_point
assert result['needs_reorder'].iloc[0] == True

print("All tests passed!")
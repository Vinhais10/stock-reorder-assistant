"""Quick sanity tests for agent_tools - no API calls."""

from agent_tools import (
    list_products_needing_reorder,
    get_product_info,
    get_reorder_point,
    get_sales_trend,
    simulate_scenario,
)


def test_list_products():
    result = list_products_needing_reorder()
    print(f"\n[list_products_needing_reorder] -> {len(result)} products")
    for p in result:
        print(f"  {p['product_id']} | shortage {p['shortage']}")
    assert isinstance(result, list)


def test_get_product_info():
    info = get_product_info("85123A")
    print(f"\n[get_product_info] -> {info}")
    assert "error" not in info
    assert info["product_id"] == "85123A"


def test_get_reorder_point():
    result = get_reorder_point("84879")
    print(f"\n[get_reorder_point] -> {result['formula']}")
    assert "reorder_point" in result


def test_get_sales_trend():
    result = get_sales_trend("85123A", days=30)
    print(f"\n[get_sales_trend] -> {result}")
    assert "total_units_sold" in result


def test_simulate_scenario():
    result = simulate_scenario("85123A", new_lead_time=20)
    print(f"\n[simulate_scenario] -> {result}")
    assert "new_reorder_point" in result


def test_unknown_product():
    result = get_product_info("XXXXXX")
    print(f"\n[unknown product] -> {result}")
    assert "error" in result


if __name__ == "__main__":
    test_list_products()
    test_get_product_info()
    test_get_reorder_point()
    test_get_sales_trend()
    test_simulate_scenario()
    test_unknown_product()
    print("\nAll tool tests passed.")

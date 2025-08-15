import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from loyalty_program import (
    register_client, add_points, place_order,
    redeem_drink, show_client
)


def test_loyalty_flow():
    data = {"clients": {}}
    cid = register_client(data, "Ana", "555", "ana@example.com")
    place_order(data, cid, "Latte")
    assert data["clients"][cid]["points"] == 1
    add_points(data, cid, 9)
    redeem_drink(data, cid, "Espresso")
    assert data["clients"][cid]["points"] == 0
    summary = show_client(data, cid)
    assert "Latte" in summary and "Espresso" in summary

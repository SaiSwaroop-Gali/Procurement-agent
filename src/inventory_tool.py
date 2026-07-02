import pandas as pd


def get_low_stock_items():

    inventory = pd.read_csv(
        "data/airline_inventory_parts.csv"
    )

    return inventory[
        inventory["current_stock"]
        < inventory["reorder_threshold"]
    ]
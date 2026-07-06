import pandas as pd


def get_supplier(supplier_id):

    suppliers = pd.read_csv(
        "data/airline_suppliers_list.csv"
    )

    return suppliers[
        suppliers["supplier_id"]
        == supplier_id
    ].iloc[0]

def get_supplier_emails():

    suppliers = pd.read_csv(
        "data/airline_suppliers_list.csv"
    )

    return set(

        suppliers["email"]
        .str.lower()
        .str.strip()

    )
import pandas as pd

from mlxtend.frequent_patterns import (
    apriori,
    association_rules
)


def create_basket_matrix(
    df: pd.DataFrame
) -> pd.DataFrame:

    sales = df[
        (df["Quantity"] > 0)
        &
        (df["UnitPrice"] > 0)
        &
        (df["DescriptionClean"].notna())
    ].copy()

    basket = (
        sales
        .drop_duplicates(
            [
                "Invoice",
                "StockCode"
            ]
        )
        .assign(
            Purchased=True
        )
        .pivot_table(
            index="Invoice",
            columns="StockCode",
            values="Purchased",
            fill_value=False
        )
    )

    return basket.astype(bool)


def find_frequent_itemsets(
    basket_matrix,
    min_support=0.01
):

    return apriori(
        basket_matrix,
        min_support=min_support,
        use_colnames=True
    )


def generate_association_rules(
    frequent_itemsets,
    min_confidence=0.2
):

    return association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=min_confidence
    )
import pandas as pd


def create_cohort_table(
    df: pd.DataFrame
) -> pd.DataFrame:

    sales = df[
        df["CustomerID"].notna()
    ].copy()

    sales["InvoiceMonth"] = (
        sales["InvoiceDate"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    first_purchase = (
        sales
        .groupby("CustomerID")
        ["InvoiceMonth"]
        .min()
        .rename("CohortMonth")
    )

    sales = sales.merge(
        first_purchase,
        on="CustomerID",
        how="left"
    )

    sales["CohortIndex"] = (
        (
            sales["InvoiceMonth"]
            .dt.year
            -
            sales["CohortMonth"]
            .dt.year
        ) * 12
        +
        (
            sales["InvoiceMonth"]
            .dt.month
            -
            sales["CohortMonth"]
            .dt.month
        )
        + 1
    )

    cohort = (
        sales
        .groupby(
            [
                "CohortMonth",
                "CohortIndex"
            ]
        )["CustomerID"]
        .nunique()
        .reset_index()
    )

    cohort.columns = [
        "CohortMonth",
        "CohortIndex",
        "Customers"
    ]

    return cohort


def create_retention_matrix(
    cohort: pd.DataFrame
) -> pd.DataFrame:

    matrix = cohort.pivot(
        index="CohortMonth",
        columns="CohortIndex",
        values="Customers"
    )

    first_period = matrix.iloc[:, 0]

    retention = (
        matrix
        .divide(
            first_period,
            axis=0
        )
        * 100
    )

    return retention
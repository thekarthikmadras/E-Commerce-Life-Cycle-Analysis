import pandas as pd


def calculate_rfm(
    df: pd.DataFrame,
    analysis_date=None
) -> pd.DataFrame:

    sales = df[
        df["CustomerID"].notna()
    ].copy()

    if analysis_date is None:
        analysis_date = (
            sales["InvoiceDate"].max()
            + pd.Timedelta(days=1)
        )

    rfm = (
        sales
        .groupby("CustomerID")
        .agg(
            Recency=(
                "InvoiceDate",
                lambda x:
                (
                    analysis_date -
                    x.max()
                ).days
            ),

            Frequency=(
                "Invoice",
                "nunique"
            ),

            Monetary=(
                "TotalPrice",
                "sum"
            )
        )
        .reset_index()
    )

    return rfm


def create_rfm_scores(
    rfm: pd.DataFrame
) -> pd.DataFrame:

    rfm = rfm.copy()

    rfm["R_Score"] = pd.qcut(
        rfm["Recency"],
        5,
        labels=[5, 4, 3, 2, 1],
        duplicates="drop"
    )

    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(
            method="first"
        ),
        5,
        labels=[1, 2, 3, 4, 5],
        duplicates="drop"
    )

    rfm["M_Score"] = pd.qcut(
        rfm["Monetary"].rank(
            method="first"
        ),
        5,
        labels=[1, 2, 3, 4, 5],
        duplicates="drop"
    )

    rfm[
        ["R_Score", "F_Score", "M_Score"]
    ] = rfm[
        ["R_Score", "F_Score", "M_Score"]
    ].astype(int)

    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(str)
        +
        rfm["F_Score"].astype(str)
        +
        rfm["M_Score"].astype(str)
    )

    return rfm


def assign_rfm_segments(
    rfm: pd.DataFrame
) -> pd.DataFrame:

    rfm = rfm.copy()

    def segment(row):

        r = row["R_Score"]
        f = row["F_Score"]
        m = row["M_Score"]

        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"

        if r >= 3 and f >= 4:
            return "Loyal Customers"

        if r >= 4 and f <= 2:
            return "New Customers"

        if r <= 2 and f >= 3:
            return "At Risk"

        if r <= 2 and f <= 2:
            return "Lost Customers"

        return "Potential Loyalists"

    rfm["Segment"] = (
        rfm.apply(
            segment,
            axis=1
        )
    )

    return rfm


def build_rfm(
    df: pd.DataFrame,
    analysis_date=None
) -> pd.DataFrame:

    rfm = calculate_rfm(
        df,
        analysis_date
    )

    rfm = create_rfm_scores(
        rfm
    )

    rfm = assign_rfm_segments(
        rfm
    )

    return rfm
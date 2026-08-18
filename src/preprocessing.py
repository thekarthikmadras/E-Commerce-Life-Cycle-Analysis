import pandas as pd
import numpy as np


def handle_missing_customer_ids(
    df: pd.DataFrame,
    strategy: str = "retain"
) -> pd.DataFrame:

    df = df.copy()

    if strategy == "drop":

        df = df[
            df["CustomerID"].notna()
        ].copy()

    elif strategy == "guest":

        df["CustomerID"] = (
            df["CustomerID"]
            .fillna("Guest")
        )

    elif strategy == "retain":
        pass

    else:
        raise ValueError(
            "strategy must be "
            "'retain', 'drop', or 'guest'"
        )

    return df


def calculate_iqr_bounds(
    series: pd.Series
):

    q1 = series.quantile(0.25)

    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr

    upper = q3 + 1.5 * iqr

    return lower, upper


def detect_iqr_outliers(
    series: pd.Series
) -> pd.Series:

    lower, upper = (
        calculate_iqr_bounds(series)
    )

    return (
        (series < lower)
        |
        (series > upper)
    )


def detect_zscore_outliers(
    series: pd.Series,
    threshold: float = 3
) -> pd.Series:

    mean = series.mean()

    std = series.std()

    if std == 0:
        return pd.Series(
            False,
            index=series.index
        )

    z_scores = (
        (series - mean) /
        std
    )

    return (
        z_scores.abs()
        > threshold
    )


def create_outlier_flags(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    df["UnitPrice_IQR_Outlier"] = (
        detect_iqr_outliers(
            df["UnitPrice"]
        )
    )

    df["UnitPrice_ZScore_Outlier"] = (
        detect_zscore_outliers(
            df["UnitPrice"]
        )
    )

    return df
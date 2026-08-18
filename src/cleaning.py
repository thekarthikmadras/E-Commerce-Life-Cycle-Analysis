import pandas as pd
import numpy as np


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "", regex=False)
    )

    rename_map = {
        "CustomerID": "CustomerID",
        "Customer_ID": "CustomerID",
        "UnitPrice": "UnitPrice",
        "Price": "UnitPrice",
    }

    df = df.rename(
        columns=rename_map
    )

    return df


def remove_exact_duplicates(
    df: pd.DataFrame
) -> pd.DataFrame:

    return (
        df
        .drop_duplicates()
        .reset_index(drop=True)
    )


def clean_descriptions(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    df["DescriptionClean"] = (
        df["Description"]
        .astype("string")
        .str.strip()
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
        .str.upper()
    )

    return df


def convert_dates(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    return df


def create_time_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    df["Year"] = (
        df["InvoiceDate"].dt.year
    )

    df["Month"] = (
        df["InvoiceDate"].dt.month
    )

    df["MonthName"] = (
        df["InvoiceDate"].dt.month_name()
    )

    df["Day"] = (
        df["InvoiceDate"].dt.day
    )

    df["DayOfWeek"] = (
        df["InvoiceDate"].dt.day_name()
    )

    df["Hour"] = (
        df["InvoiceDate"].dt.hour
    )

    return df


def create_total_price(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    df["TotalPrice"] = (
        df["Quantity"] *
        df["UnitPrice"]
    )

    return df


def identify_returns(
    df: pd.DataFrame
) -> pd.DataFrame:

    return df[
        df["Quantity"] < 0
    ].copy()


def identify_valid_sales(
    df: pd.DataFrame
) -> pd.DataFrame:

    sales = df[
        df["Quantity"] > 0
    ].copy()

    sales = sales[
        sales["UnitPrice"] > 0
    ].copy()

    return sales.reset_index(
        drop=True
    )


def clean_retail_data(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = standardize_columns(df)

    df = remove_exact_duplicates(df)

    df = convert_dates(df)

    df = clean_descriptions(df)

    df = create_time_features(df)

    df = create_total_price(df)

    return df.reset_index(
        drop=True
    )
from pathlib import Path

import pandas as pd

from src.cleaning import (
    clean_retail_data,
    identify_returns,
    identify_valid_sales
)

from src.utils import (
    get_raw_data_dir,
    get_processed_data_dir
)


def main():

    print("=" * 70)
    print("E-COMMERCE ANALYSIS PIPELINE")
    print("=" * 70)

    raw_path = (
        get_raw_data_dir()
        / "online_retail_II.xlsx"
    )

    processed_dir = (
        get_processed_data_dir()
    )

    processed_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\n[1/5] Loading raw dataset...")

    df = pd.read_excel(
        raw_path
    )

    print(
        f"Loaded {len(df):,} rows"
    )

    print("\n[2/5] Cleaning dataset...")

    cleaned = clean_retail_data(df)

    print(
        f"Cleaned rows: "
        f"{len(cleaned):,}"
    )

    print("\n[3/5] Separating returns...")

    returns = identify_returns(
        cleaned
    )

    print(
        f"Returns: "
        f"{len(returns):,}"
    )

    print("\n[4/5] Creating sales dataset...")

    sales = identify_valid_sales(
        cleaned
    )

    print(
        f"Valid sales: "
        f"{len(sales):,}"
    )

    print("\n[5/5] Saving processed data...")

    cleaned_path = (
        processed_dir
        / "online_retail_cleaned.csv"
    )

    returns_path = (
        processed_dir
        / "online_retail_returns.csv"
    )

    sales_path = (
        processed_dir
        / "online_retail_sales.csv"
    )

    cleaned.to_csv(
        cleaned_path,
        index=False
    )

    returns.to_csv(
        returns_path,
        index=False
    )

    sales.to_csv(
        sales_path,
        index=False
    )

    print(
        "\nPipeline completed successfully."
    )

    print(
        f"\nCleaned data: {cleaned_path}"
    )

    print(
        f"Returns: {returns_path}"
    )

    print(
        f"Sales: {sales_path}"
    )


if __name__ == "__main__":
    main()
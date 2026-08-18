import matplotlib.pyplot as plt
import seaborn as sns


def plot_monthly_revenue(
    monthly_revenue
):

    fig, ax = plt.subplots(
        figsize=(14, 7)
    )

    sns.lineplot(
        data=monthly_revenue,
        x="InvoiceDate",
        y="TotalPrice",
        marker="o",
        ax=ax
    )

    ax.set_title(
        "Monthly Revenue"
    )

    ax.set_xlabel("Month")

    ax.set_ylabel(
        "Revenue (£)"
    )

    fig.tight_layout()

    return fig


def plot_top_products(
    product_df,
    n=10
):

    data = (
        product_df
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(n)
        .sort_values("Revenue")
    )

    fig, ax = plt.subplots(
        figsize=(12, 7)
    )

    sns.barplot(
        data=data,
        x="Revenue",
        y="DescriptionClean",
        ax=ax
    )

    ax.set_title(
        f"Top {n} Products by Revenue"
    )

    ax.set_xlabel(
        "Revenue (£)"
    )

    ax.set_ylabel(
        "Product"
    )

    fig.tight_layout()

    return fig


def plot_customer_segments(
    rfm_df
):

    counts = (
        rfm_df["Segment"]
        .value_counts()
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        "Customer Segments"
    )

    ax.set_xlabel(
        "Segment"
    )

    ax.set_ylabel(
        "Customers"
    )

    fig.tight_layout()

    return fig
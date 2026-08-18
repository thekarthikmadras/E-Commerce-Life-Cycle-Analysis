import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

warnings.filterwarnings("ignore")


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_sales_data():

    path = (
        PROCESSED_DIR /
        "online_retail_cleaned.csv"
    )

    return pd.read_csv(
        path,
        parse_dates=["InvoiceDate"]
    )


@st.cache_data
def load_returns_data():

    path = (
        PROCESSED_DIR /
        "online_retail_returns.csv"
    )

    return pd.read_csv(
        path,
        parse_dates=["InvoiceDate"]
    )


@st.cache_data
def load_product_data():

    path = (
        REPORTS_DIR /
        "product_analysis.csv"
    )

    return pd.read_csv(path)


@st.cache_data
def load_country_data():

    path = (
        REPORTS_DIR /
        "country_analysis.csv"
    )

    return pd.read_csv(path)


@st.cache_data
def load_rfm_data():

    path = (
        REPORTS_DIR /
        "rfm_analysis.csv"
    )

    return pd.read_csv(path)


@st.cache_data
def load_rules():

    path = (
        REPORTS_DIR /
        "strong_association_rules.csv"
    )

    return pd.read_csv(path)


# ============================================================
# LOAD DATA
# ============================================================

df = load_sales_data()
returns_df = load_returns_data()
product_df = load_product_data()
country_df = load_country_data()
rfm_df = load_rfm_data()
rules_df = load_rules()


# ============================================================
# TITLE
# ============================================================

st.title(
    "🛒 E-Commerce Analytics Dashboard"
)

st.markdown(
    """
    **Full Life-Cycle Analysis of the Online Retail II Dataset**

    Explore sales performance, customers, products,
    returns and purchasing patterns.
    """
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Executive Overview",
        "Sales Analysis",
        "Customer Analysis",
        "Product Analysis",
        "Returns Analysis",
        "Basket Analysis"
    ]
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.header("Executive Overview")

    total_revenue = df["TotalPrice"].sum()

    total_orders = df["Invoice"].nunique()

    total_customers = df["CustomerID"].nunique()

    total_products = df["StockCode"].nunique()

    aov = (
        total_revenue /
        total_orders
    )

    return_units = (
        returns_df["Quantity"]
        .abs()
        .sum()
    )

    total_units = df["Quantity"].sum()

    return_rate = (
        return_units /
        total_units *
        100
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Revenue",
        f"£{total_revenue:,.0f}"
    )

    col2.metric(
        "Orders",
        f"{total_orders:,}"
    )

    col3.metric(
        "Customers",
        f"{total_customers:,}"
    )

    col4.metric(
        "Products",
        f"{total_products:,}"
    )

    col5.metric(
        "Return Rate",
        f"{return_rate:.2f}%"
    )

    st.divider()

    # --------------------------------------------------------
    # Monthly revenue
    # --------------------------------------------------------

    monthly = (
        df
        .set_index("InvoiceDate")
        .resample("ME")["TotalPrice"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="InvoiceDate",
        y="TotalPrice",
        markers=True,
        title="Monthly Revenue"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (£)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # Top countries / products
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        top_countries = (
            country_df
            .sort_values(
                "Revenue",
                ascending=False
            )
            .head(10)
        )

        fig_country = px.bar(
            top_countries,
            x="Revenue",
            y="Country",
            orientation="h",
            title="Top Countries by Revenue"
        )

        st.plotly_chart(
            fig_country,
            use_container_width=True
        )

    with col2:

        top_products = (
            product_df
            .sort_values(
                "Revenue",
                ascending=False
            )
            .head(10)
            .sort_values("Revenue")
        )

        fig_product = px.bar(
            top_products,
            x="Revenue",
            y="DescriptionClean",
            orientation="h",
            title="Top Products by Revenue"
        )

        st.plotly_chart(
            fig_product,
            use_container_width=True
        )


# ============================================================
# SALES ANALYSIS
# ============================================================

elif page == "Sales Analysis":

    st.header("📈 Sales Analysis")

    min_date = df["InvoiceDate"].min()
    max_date = df["InvoiceDate"].max()

    start_date, end_date = st.date_input(
        "Select date range",
        value=(
            min_date.date(),
            max_date.date()
        )
    )

    sales = df[
        (
            df["InvoiceDate"].dt.date
            >= start_date
        )
        &
        (
            df["InvoiceDate"].dt.date
            <= end_date
        )
    ].copy()

    revenue = sales["TotalPrice"].sum()

    orders = sales["Invoice"].nunique()

    aov = (
        revenue /
        orders
        if orders > 0
        else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Revenue",
        f"£{revenue:,.0f}"
    )

    col2.metric(
        "Orders",
        f"{orders:,}"
    )

    col3.metric(
        "AOV",
        f"£{aov:,.2f}"
    )

    monthly = (
        sales
        .set_index("InvoiceDate")
        .resample("ME")["TotalPrice"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="InvoiceDate",
        y="TotalPrice",
        markers=True,
        title="Revenue Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Day of week

    sales["DayOfWeek"] = (
        sales["InvoiceDate"]
        .dt.day_name()
    )

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    weekday_sales = (
        sales
        .groupby("DayOfWeek")["TotalPrice"]
        .sum()
        .reindex(weekday_order)
        .reset_index()
    )

    fig = px.bar(
        weekday_sales,
        x="DayOfWeek",
        y="TotalPrice",
        title="Revenue by Day of Week"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

elif page == "Customer Analysis":

    st.header("👥 Customer Analysis")

    if "Segment" in rfm_df.columns:

        segment_counts = (
            rfm_df["Segment"]
            .value_counts()
            .reset_index()
        )

        segment_counts.columns = [
            "Segment",
            "Customers"
        ]

        fig = px.bar(
            segment_counts,
            x="Segment",
            y="Customers",
            title="Customer Segments"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.warning(
            "RFM segment column was not found."
        )

    st.subheader(
        "Top Customers by Monetary Value"
    )

    monetary_column = None

    for column in [
        "Monetary",
        "MonetaryValue",
        "MonetaryTotal"
    ]:

        if column in rfm_df.columns:
            monetary_column = column
            break

    if monetary_column:

        top_customers = (
            rfm_df
            .sort_values(
                monetary_column,
                ascending=False
            )
            .head(20)
        )

        st.dataframe(
            top_customers,
            use_container_width=True
        )


# ============================================================
# PRODUCT ANALYSIS
# ============================================================

elif page == "Product Analysis":

    st.header("📦 Product Analysis")

    metric = st.selectbox(
        "Rank products by",
        [
            "Revenue",
            "UnitsSold",
            "Orders",
            "Customers"
        ]
    )

    top_n = st.slider(
        "Number of products",
        5,
        30,
        10
    )

    top_products = (
        product_df
        .sort_values(
            metric,
            ascending=False
        )
        .head(top_n)
        .sort_values(metric)
    )

    fig = px.bar(
        top_products,
        x=metric,
        y="DescriptionClean",
        orientation="h",
        title=f"Top {top_n} Products by {metric}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Revenue vs Volume"
    )

    scatter_df = product_df[
        product_df["UnitsSold"] > 0
    ].copy()

    fig = px.scatter(
        scatter_df,
        x="UnitsSold",
        y="Revenue",
        hover_name="DescriptionClean",
        size="RevenuePerUnit",
        log_x=True,
        log_y=True,
        title="Product Revenue vs Volume"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Product Data"
    )

    st.dataframe(
        product_df.sort_values(
            "Revenue",
            ascending=False
        ).head(100),
        use_container_width=True
    )


# ============================================================
# RETURNS ANALYSIS
# ============================================================

elif page == "Returns Analysis":

    st.header("↩️ Returns Analysis")

    total_return_value = (
        returns_df["ReturnValue"]
        .sum()
    )

    total_return_units = (
        returns_df["Quantity"]
        .abs()
        .sum()
    )

    total_sales_units = (
        df["Quantity"].sum()
    )

    return_rate = (
        total_return_units /
        total_sales_units *
        100
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Returned Units",
        f"{total_return_units:,.0f}"
    )

    col2.metric(
        "Return Value",
        f"£{total_return_value:,.0f}"
    )

    col3.metric(
        "Return Rate",
        f"{return_rate:.2f}%"
    )

    st.subheader(
        "Highest Return-Rate Products"
    )

    return_products = (
        product_df[
            product_df["UnitsSold"] >= 50
        ]
        .sort_values(
            "ReturnRate",
            ascending=False
        )
        .head(15)
        .sort_values("ReturnRate")
    )

    fig = px.bar(
        return_products,
        x="ReturnRate",
        y="DescriptionClean",
        orientation="h",
        title="Highest Product Return Rates"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Return Data"
    )

    st.dataframe(
        returns_df.head(100),
        use_container_width=True
    )


# ============================================================
# BASKET ANALYSIS
# ============================================================

elif page == "Basket Analysis":

    st.header("🛍️ Basket Analysis")

    st.markdown(
        """
        Association rules identify products that tend
        to be purchased together.
        """
    )

    min_lift = st.slider(
        "Minimum Lift",
        1.0,
        10.0,
        1.5,
        0.1
    )

    min_confidence = st.slider(
        "Minimum Confidence",
        0.1,
        1.0,
        0.2,
        0.05
    )

    filtered_rules = rules_df[
        (
            rules_df["Lift"]
            >= min_lift
        )
        &
        (
            rules_df["Confidence"]
            >= min_confidence
        )
    ].copy()

    st.metric(
        "Matching Rules",
        len(filtered_rules)
    )

    if len(filtered_rules) > 0:

        filtered_rules["Rule"] = (
            filtered_rules["Antecedent"]
            + " → "
            + filtered_rules["Consequent"]
        )

        display_rules = (
            filtered_rules
            .sort_values(
                "Lift",
                ascending=False
            )
            .head(50)
        )

        fig = px.bar(
            display_rules.sort_values("Lift"),
            x="Lift",
            y="Rule",
            orientation="h",
            title="Association Rules by Lift"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            display_rules[
                [
                    "Antecedent",
                    "Consequent",
                    "Support",
                    "Confidence",
                    "Lift"
                ]
            ],
            use_container_width=True
        )

    else:

        st.info(
            "No rules match the selected thresholds."
        )
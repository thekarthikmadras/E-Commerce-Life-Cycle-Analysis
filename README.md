# 🛒 E-Commerce Life-Cycle Analysis

> End-to-end data analysis of a messy real-world retail transaction dataset — from raw data cleaning to customer segmentation, cohort analysis, basket analysis, and an interactive Streamlit dashboard.

---

## 📌 Overview

This project performs a complete analytical lifecycle on the **Online Retail II** dataset from the UCI Machine Learning Repository.

Unlike clean educational datasets such as Iris or Titanic, the dataset contains real-world data-quality problems including:

- Missing customer identifiers
- Duplicate records
- Negative quantities representing returns
- Cancelled invoices
- Zero and anomalous prices
- Inconsistent product descriptions
- Extreme values

The project demonstrates how a data analyst / data scientist can transform this raw data into actionable business insights.

---

# 🎯 Objectives

The project answers questions such as:

- How does revenue change over time?
- Which products generate the most revenue?
- Which countries generate the most sales?
- Which customers are most valuable?
- Which customers are at risk of becoming inactive?
- How well are customers retained?
- Which products have high return rates?
- Which products are frequently purchased together?
- Where are the strongest cross-selling opportunities?

---

# 🧰 Tech Stack

- Python
- pandas
- NumPy
- SciPy
- matplotlib
- seaborn
- missingno
- scikit-learn
- mlxtend
- Streamlit
- Plotly
- Jupyter Notebook

---

# 📊 Dataset

**Online Retail II**

Source:

UCI Machine Learning Repository

The dataset contains approximately 1 million transaction records from a UK-based online retailer covering 2009–2011.

The raw dataset is intentionally not committed to Git because of its size.

Download the dataset from the UCI Machine Learning Repository and place it at:

```text
data/raw/online_retail_II.xlsx
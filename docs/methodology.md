# Methodology

## 1. Data Understanding

The raw Online Retail II dataset was inspected for:

- Shape
- Data types
- Missing values
- Duplicate records
- Unique values
- Numerical distributions
- Invalid values

---

## 2. Data Cleaning

### Duplicate Records

Exact duplicate transactions were identified and removed where appropriate.

### Missing Customer IDs

Missing customer identifiers were not imputed because a fabricated customer identity would introduce false customer-level relationships.

Transactions without customer IDs were therefore excluded from customer-level analysis while remaining available for transaction-level analysis where appropriate.

### Returns

Negative quantities were interpreted as returns/cancellations rather than automatically treating them as data errors.

Returns were separated for dedicated return analysis.

### Prices

Zero, negative, and extreme prices were investigated.

IQR and z-score methods were used to understand price outliers.

### Text Standardization

Product descriptions were normalized by:

- Removing leading/trailing whitespace
- Standardizing casing
- Creating cleaned descriptions
- Investigating near-duplicate descriptions

---

## 3. Exploratory Data Analysis

The analysis examined:

- Revenue
- Quantity
- Unit price
- Orders
- Customers
- Countries
- Time trends
- Missingness
- Correlations

---

## 4. RFM Analysis

Customers were evaluated using:

### Recency

Days since the customer's most recent purchase.

### Frequency

Number of unique invoices/orders.

### Monetary

Total customer revenue.

Customers were assigned RFM scores and grouped into meaningful customer segments.

---

## 5. Cohort Analysis

Customers were grouped according to their first purchase period.

Retention was calculated by comparing subsequent purchasing activity against the customer's acquisition cohort.

---

## 6. Product Analysis

Products were evaluated by:

- Revenue
- Units sold
- Orders
- Customers
- Average price
- Return rate

Pareto analysis was used to examine revenue concentration.

---

## 7. Country Analysis

Countries were compared using:

- Revenue
- Orders
- Customers
- Units
- Average order value
- Return rate

---

## 8. Basket Analysis

Transaction-level baskets were converted into a binary product matrix.

Apriori was used to identify frequent itemsets.

Association rules were evaluated using:

- Support
- Confidence
- Lift

Rules with extremely low support were avoided to reduce the likelihood of misleading associations.

---

## 9. Business Interpretation

Statistical findings were translated into practical recommendations involving:

- Customer retention
- Product management
- Inventory planning
- Cross-selling
- Returns management
- Geographic expansion
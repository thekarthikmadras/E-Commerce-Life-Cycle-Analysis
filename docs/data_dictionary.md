# Data Dictionary

## Online Retail II

The dataset contains transactional records from a UK-based online retailer covering 2009–2011.

| Column | Description |
|---|---|
| Invoice | Unique invoice/transaction identifier |
| StockCode | Unique product identifier |
| Description | Product description |
| Quantity | Number of units purchased |
| InvoiceDate | Date and time of transaction |
| Price / UnitPrice | Price per unit |
| Customer ID / CustomerID | Customer identifier |
| Country | Customer's country |

## Derived Variables

| Variable | Description |
|---|---|
| TotalPrice | Quantity × UnitPrice |
| ReturnValue | Absolute value of returned quantity × unit price |
| Year | Transaction year |
| Month | Transaction month |
| Day | Day of month |
| DayOfWeek | Day of week |
| Hour | Transaction hour |

## Important Data Quality Issues

The original dataset contains:

- Missing Customer IDs
- Duplicate transactions
- Negative quantities
- Zero prices
- Negative prices
- Cancelled invoices
- Inconsistent descriptions
- Extreme price values

These issues were investigated during the data-cleaning stage rather than silently removed.
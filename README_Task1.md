
# Task 1: Sales Data Analysis

## 1. Project Overview
This project analyses the Online Retail dataset to understand sales
performance, revenue trends, popular products, and country-wise sales.

## 2. Objectives
- Calculate total revenue, orders, quantity sold, and Average Order Value.
- Analyse monthly and quarterly revenue trends.
- Identify top-selling products by revenue and quantity.
- Compare sales revenue across countries.
- Provide data-driven business recommendations.

## 3. Dataset
Source: UCI Machine Learning Repository - Online Retail Dataset
https://archive.ics.uci.edu/dataset/352/online+retail

The dataset contains invoice details, product descriptions, quantities,
unit prices, invoice dates, customer IDs, and countries.

## 4. Data Preparation
- Converted invoice dates and numeric columns to appropriate data types.
- Excluded cancelled invoices identified by invoice numbers beginning with C.
- Excluded rows with non-positive quantities or unit prices.
- Calculated revenue as Quantity multiplied by UnitPrice.

## 5. Analysis Performed
- Key performance indicator (KPI) summary
- Monthly revenue trend
- Quarterly revenue trend
- Seasonal revenue analysis
- Top 10 products by revenue
- Top 10 products by quantity sold
- Top 10 countries by revenue

## 6. Business Recommendations
- Plan inventory using historical high-revenue periods.
- Maintain sufficient stock of products generating high revenue.
- Study high-performing markets to guide marketing decisions.
- Investigate low-performing periods and products for improvement.

## 7. Limitations
The dataset does not provide product cost information. Therefore,
actual profit and profit margins cannot be calculated reliably.
Revenue must not be interpreted as profit.

Seasonal patterns should be interpreted cautiously because the dataset
covers a limited historical period.

## 8. Tools Used
- Python
- Pandas
- Matplotlib
- Google Colab

## 9. Output Charts
The Task1_Charts folder contains the exported sales analysis charts.

## 10. Conclusion
The analysis provides an overview of retail sales performance and helps
identify revenue trends, popular products, and important markets.
Business decisions should be based on the calculated results and
the limitations of the available data.

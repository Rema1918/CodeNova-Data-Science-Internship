
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Online Retail Sales Dashboard",
    layout="wide"
)

st.title("Online Retail Sales Dashboard")
st.write("Interactive analysis of online retail sales")

@st.cache_data
def load_data():
    data = pd.read_csv("Online_Retail_Sample.csv")
    data["InvoiceDate"] = pd.to_datetime(
        data["InvoiceDate"], errors="coerce"
    )
    data["Revenue"] = data["Quantity"] * data["UnitPrice"]
    return data

# Load dataset
df = load_data()

# Country filter
countries = ["All"] + sorted(df["Country"].dropna().unique().tolist())
selected_country = st.selectbox("Select Country", countries)

if selected_country == "All":
    data = df.copy()
else:
    data = df[df["Country"] == selected_country].copy()

# Dashboard metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"£{data['Revenue'].sum():,.2f}")
col2.metric("Total Orders", f"{data['InvoiceNo'].nunique():,}")
col3.metric("Quantity Sold", f"{data['Quantity'].sum():,}")

# Monthly sales trend
data["Month"] = data["InvoiceDate"].dt.to_period("M").astype(str)

st.subheader("Monthly Sales Trend")
st.line_chart(data.groupby("Month")["Revenue"].sum())

# Top products
st.subheader("Top 10 Products by Revenue")
top_products = (
    data.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
st.bar_chart(top_products)

# Country-wise sales
st.subheader("Country-wise Sales")
country_sales = (
    data.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
st.bar_chart(country_sales)

# Preview
st.subheader("Sales Data Preview")
st.dataframe(data.head(100))


st.subheader("Country-wise Sales")
st.bar_chart(
    data.groupby("Country")["Revenue"]
    .sum().sort_values(ascending=False).head(10)
)

st.subheader("Sales Data Preview")
st.dataframe(data.head(100))

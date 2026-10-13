import streamlit as st
import pandas as pd
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("Online Retail Sales Dashboard")
st.write("Interactive analysis of online retail sales")

@st.cache_data
def load_data():
    pd.read_csv("Online_Retail_Sample.csv")
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])
    data["Revenue"] = data["Quantity"] * data["UnitPrice"]
    return data

df = load_data()

countries = ["All"] + sorted(df["Country"].dropna().unique().tolist())
selected_country = st.selectbox("Select Country", countries)

data = df if selected_country == "All" else df[df["Country"] == selected_country].copy()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"£{data['Revenue'].sum():,.2f}")
col2.metric("Total Orders", f"{data['InvoiceNo'].nunique():,}")
col3.metric("Quantity Sold", f"{data['Quantity'].sum():,}")

data = data.copy()
data["Month"] = data["InvoiceDate"].dt.to_period("M").astype(str)

st.subheader("Monthly Sales Trend")
st.line_chart(data.groupby("Month")["Revenue"].sum())

st.subheader("Top 10 Products by Revenue")
st.bar_chart(
    data.groupby("Description")["Revenue"]
    .sum().sort_values(ascending=False).head(10)
)

st.subheader("Country-wise Sales")
st.bar_chart(
    data.groupby("Country")["Revenue"]
    .sum().sort_values(ascending=False).head(10)
)

st.subheader("Sales Data Preview")
st.dataframe(data.head(100))

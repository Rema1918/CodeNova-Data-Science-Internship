
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Online Retail Sales Analytics")
st.caption("Interactive dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("Online_Retail_Sample.csv")
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df = df.dropna(subset=["InvoiceDate", "Quantity", "UnitPrice"])
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔎 Dashboard Filters")

countries = sorted(df["Country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    default=countries
)

min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

product_search = st.sidebar.text_input(
    "Search Product",
    placeholder="Enter product name..."
)

filtered = df.copy()

if selected_countries:
    filtered = filtered[
        filtered["Country"].isin(selected_countries)
    ]
else:
    filtered = filtered.iloc[0:0]

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["InvoiceDate"].dt.date >= start_date) &
        (filtered["InvoiceDate"].dt.date <= end_date)
    ]

if product_search.strip():
    filtered = filtered[
        filtered["Description"].str.contains(
            product_search, case=False, na=False
        )
    ]

st.caption(f"Showing {len(filtered):,} transaction rows")

# KPI cards
revenue = filtered["Revenue"].sum()
orders = filtered["InvoiceNo"].nunique()
quantity = filtered["Quantity"].sum()

if "CustomerID" in filtered.columns:
    customers = filtered["CustomerID"].nunique()
else:
    customers = 0

aov = revenue / orders if orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Total Revenue", f"£{revenue:,.2f}")
c2.metric("🧾 Total Orders", f"{orders:,}")
c3.metric("📦 Quantity Sold", f"{quantity:,.0f}")
c4.metric("👥 Unique Customers", f"{customers:,}")

st.metric("Average Order Value", f"£{aov:,.2f}")

if filtered.empty:
    st.warning("No data found. Change the filters and try again.")
else:
    # Monthly trend
    st.subheader("📈 Monthly Sales Trend")
    monthly = (
        filtered.assign(
            Month=filtered["InvoiceDate"].dt.to_period("M").astype(str)
        )
        .groupby("Month", as_index=False)["Revenue"].sum()
    )

    fig_month = px.line(
        monthly,
        x="Month",
        y="Revenue",
        markers=True,
        title="Revenue by Month",
        hover_data={"Revenue": ":,.2f"}
    )
    fig_month.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (£)"
    )
    st.plotly_chart(fig_month, use_container_width=True)

    left, right = st.columns(2)

    # Product chart
    with left:
        st.subheader("🏆 Top 10 Products")
        products = (
            filtered.groupby("Description", as_index=False)["Revenue"]
            .sum()
            .sort_values("Revenue", ascending=False)
            .head(10)
            .sort_values("Revenue")
        )

        fig_products = px.bar(
            products,
            x="Revenue",
            y="Description",
            orientation="h",
            title="Products by Revenue",
            hover_data={"Revenue": ":,.2f"}
        )
        st.plotly_chart(fig_products, use_container_width=True)

    # Country chart
    with right:
        st.subheader("🌍 Country-wise Sales")
        country_sales = (
            filtered.groupby("Country", as_index=False)["Revenue"]
            .sum()
            .sort_values("Revenue", ascending=False)
            .head(10)
        )

        fig_country = px.bar(
            country_sales,
            x="Country",
            y="Revenue",
            title="Top Countries by Revenue",
            hover_data={"Revenue": ":,.2f"}
        )
        st.plotly_chart(fig_country, use_container_width=True)

    # Data table
    st.subheader("📋 Filtered Transaction Details")
    st.dataframe(filtered, use_container_width=True)

    # Download filtered results
    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered Data (CSV)",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )

st.sidebar.success("Change filters to update the dashboard.")

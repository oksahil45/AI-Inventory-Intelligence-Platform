
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FORESIGHT", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("online_retail_II.xlsx")
    cols = {c.lower(): c for c in df.columns}

    df["InvoiceDate"] = pd.to_datetime(df[cols["invoicedate"]], errors="coerce")
    qty = cols.get("quantity")
    price = cols.get("price") or cols.get("unitprice")

    df["Quantity"] = pd.to_numeric(df[qty], errors="coerce")
    df["Price"] = pd.to_numeric(df[price], errors="coerce")
    df = df.dropna(subset=["InvoiceDate"])
    df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]
    df["Revenue"] = df["Quantity"] * df["Price"]
    return df

df = load_data()

st.title("📦 Project FORESIGHT")

page = st.sidebar.radio("Navigation",[
"Executive Summary",
"Sales Analysis",
"Product Performance",
"Inventory Risk",
"Customer Analytics",
"Geographic Analysis"
])

if page=="Executive Summary":
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Revenue", f"₹ {df['Revenue'].sum():,.0f}")
    c2.metric("Transactions", len(df))
    c3.metric("Products", df['StockCode'].nunique() if 'StockCode' in df.columns else 0)
    c4.metric("Countries", df['Country'].nunique() if 'Country' in df.columns else 0)

elif page=="Sales Analysis":
    d=df.groupby(df["InvoiceDate"].dt.date)["Revenue"].sum().reset_index()
    st.plotly_chart(px.line(d,x="InvoiceDate",y="Revenue"),use_container_width=True)

elif page=="Product Performance":
    if "Description" in df.columns:
        top=df.groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(10)
        st.plotly_chart(px.bar(top),use_container_width=True)

elif page=="Inventory Risk":
    if "Description" in df.columns:
        p=df.groupby("Description")["Quantity"].sum().reset_index()
        p["Estimated_Stock"]=p["Quantity"]*2
        st.dataframe(p.head(100))

elif page=="Customer Analytics":
    cust=[c for c in df.columns if "Customer" in c]
    if cust:
        top=df.groupby(cust[0])["Revenue"].sum().sort_values(ascending=False).head(20)
        st.plotly_chart(px.bar(top),use_container_width=True)

elif page=="Geographic Analysis":
    if "Country" in df.columns:
        c=df.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(20)
        st.plotly_chart(px.bar(c),use_container_width=True)

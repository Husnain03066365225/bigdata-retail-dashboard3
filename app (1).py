
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Retail Big Data", layout="wide")
st.title("🛒 Big Data Analysis - Online Retail Dashboard")
st.subheader("1.07 Million Transactions Analysis")
st.caption("Muhammad Husnain | Big Data Analysis Course")

uploaded_file = st.file_uploader("Upload your **online retail.csv** file", type="csv")

if uploaded_file is not None:
    with st.spinner("Processing..."):
        df = pd.read_csv(uploaded_file, encoding='latin1')

        df_clean = df[~df['Invoice'].astype(str).str.startswith('C')].copy()
        df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['Price'] > 0)]
        df_clean = df_clean.dropna(subset=['Customer ID', 'Description', 'Country'])

        st.success(f"✅ Processed **{len(df_clean):,}** records!")

        tab1, tab2, tab3 = st.tabs(["Top 10 Products", "Revenue by Country", "Monthly Trend"])

        with tab1:
            top = df_clean.groupby('Description')['Quantity'].sum().reset_index()
            top = top.sort_values('Quantity', ascending=False).head(10)
            st.dataframe(top, use_container_width=True)
            fig, ax = plt.subplots(figsize=(10,6))
            sns.barplot(data=top, x='Quantity', y='Description', palette='Blues_d')
            st.pyplot(fig)

        with tab2:
            revenue = df_clean.groupby('Country').apply(
                lambda x: (x['Quantity'] * x['Price']).sum()
            ).reset_index(name='Total_Revenue')
            revenue = revenue.sort_values('Total_Revenue', ascending=False).head(10)
            st.dataframe(revenue, use_container_width=True)

        with tab3:
            df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'], errors='coerce')
            df_clean['Year_Month'] = df_clean['InvoiceDate'].dt.strftime('%Y-%m')
            monthly = df_clean.groupby('Year_Month').apply(
                lambda x: (x['Quantity'] * x['Price']).sum()
            ).reset_index(name='Revenue')
            st.line_chart(monthly.set_index('Year_Month'))
else:
    st.info("Please upload online retail.csv file")

# app.py (safe fallback version)

import streamlit as st
import pandas as pd
import plotly.express as px
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components

st.set_page_config(page_title="DashFlow", layout="wide")
st.title("Upload CSV → Instant Dashboard")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader(" Data Preview")
    st.dataframe(df.head())

    # EDA Report
    with st.spinner("Generating EDA report..."):
        profile = ProfileReport(df, title="Auto Report", explorative=True)
        profile.to_file("report.html")
        with open("report.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=600, scrolling=True)

    # Charts
    num_cols = df.select_dtypes(include='number').columns
    cat_cols = df.select_dtypes(include='object').columns

    st.subheader(" Auto Charts")
    if len(num_cols) >= 2:
        fig = px.bar(df, x=num_cols[0], y=num_cols[1], title="Auto Bar Chart")
        st.plotly_chart(fig, use_container_width=True)

    if len(cat_cols) > 0 and len(num_cols) > 0:
        pie_df = df.groupby(cat_cols[0])[num_cols[0]].sum().reset_index()
        fig2 = px.pie(pie_df, names=cat_cols[0], values=num_cols[0], title="Auto Pie Chart")
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("Upload a CSV file to start the analysis.")

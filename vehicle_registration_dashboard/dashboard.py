import streamlit as st
import plotly.express as px
import pandas as pd
from data_processor import load_category_data, load_manufacturer_data, calculate_growth

st.title("Vehicle Registration Dashboard")
st.markdown("Investor-focused view of growth trends in Indian vehicle registrations (2W/3W/4W and manufacturers). Data: Synthetic, mimicking Vahan.")

tab1, tab2 = st.tabs(["By Vehicle Category", "By Manufacturer"])

with tab1:
    df_cat = load_category_data()
    categories = sorted(df_cat['category'].unique())
    selected_categories = st.multiselect("Filter by Vehicle Category", categories, default=categories)
    min_date, max_date = df_cat['date'].min().date(), df_cat['date'].max().date()
    start_date, end_date = st.date_input("Select Date Range", [min_date, max_date])

    filtered_df = df_cat[
        (df_cat['category'].isin(selected_categories)) &
        (df_cat['date'] >= pd.to_datetime(start_date)) &
        (df_cat['date'] <= pd.to_datetime(end_date))
    ]

    if not filtered_df.empty:
        trend_df = filtered_df.groupby(['date', 'category'])['registrations'].sum().reset_index()
        fig_trend = px.line(trend_df, x='date', y='registrations', color='category', title="Registration Trends")
        st.plotly_chart(fig_trend)

        growth_type = st.selectbox("Select Growth Type", ["YoY (Annual)", "QoQ (Quarterly)"], key="cat_growth")
        level = 'Y' if growth_type == "YoY (Annual)" else 'Q'
        growth_df = calculate_growth(filtered_df, 'category', level)
        fig_growth = px.bar(growth_df, x='date', y='growth', color='category', title=f"{growth_type} Growth (%)")
        st.plotly_chart(fig_growth)
    else:
        st.warning("No data available for selected filters.")

with tab2:
    df_man = load_manufacturer_data()
    manufacturers = sorted(df_man['maker'].unique())
    selected_manufacturers = st.multiselect("Filter by Manufacturer", manufacturers, default=manufacturers[:5])
    min_date, max_date = df_man['date'].min().date(), df_man['date'].max().date()
    start_date, end_date = st.date_input("Select Date Range", [min_date, max_date], key="man_date")

    filtered_df = df_man[
        (df_man['maker'].isin(selected_manufacturers)) &
        (df_man['date'] >= pd.to_datetime(start_date)) &
        (df_man['date'] <= pd.to_datetime(end_date))
    ]

    if not filtered_df.empty:
        trend_df = filtered_df.groupby(['date', 'maker'])['registrations'].sum().reset_index()
        fig_trend = px.line(trend_df, x='date', y='registrations', color='maker', title="Registration Trends")
        st.plotly_chart(fig_trend)

        growth_type = st.selectbox("Select Growth Type", ["YoY (Annual)", "QoQ (Quarterly)"], key="man_growth")
        level = 'Y' if growth_type == "YoY (Annual)" else 'Q'
        growth_df = calculate_growth(filtered_df, 'maker', level)
        fig_growth = px.bar(growth_df, x='date', y='growth', color='maker', title=f"{growth_type} Growth (%)")
        st.plotly_chart(fig_growth)
    else:
        st.warning("No data available for selected filters.")
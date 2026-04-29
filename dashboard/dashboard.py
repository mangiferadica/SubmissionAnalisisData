import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title
st.set_page_config(page_title="Air Quality Dashboard - Guanyuan", layout="wide")


@st.cache_data
def load_data():
    # Pastikan file CSV ada di folder yang sama dengan script ini
    df = pd.read_csv('PRSA_Data_Guanyuan_20130301-20170228.csv')
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

    # Cleaning: Interpolasi data kosong pada kolom numerik
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = df[numeric_cols].interpolate(method='linear')
    return df


try:
    df = load_data()

    # Sidebar
    with st.sidebar:
        st.title("Proyek Analisis Data")
        st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

        # Filter Rentang Waktu
        min_date = df['datetime'].min().date()
        max_date = df['datetime'].max().date()

        # Input rentang waktu (mengembalikan tuple)
        date_range = st.date_input(
            label='Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

    # Logika filter jika user memilih rentang (start dan end)
    if len(date_range) == 2:
        start_date, end_date = date_range
        main_df = df[(df['datetime'].dt.date >= start_date) &
                     (df['datetime'].dt.date <= end_date)]
    else:
        main_df = df.copy()

    # Main Dashboard
    st.title("Air Quality Dashboard (Guanyuan Station) 💨")

    # Metrik Utama
    col1, col2 = st.columns(2)
    with col1:
        avg_pm25 = round(main_df['PM2.5'].mean(), 2)
        st.metric("Rata-rata PM2.5", value=f"{avg_pm25} µg/m³")
    with col2:
        max_pm25 = main_df['PM2.5'].max()
        st.metric("PM2.5 Tertinggi", value=f"{max_pm25} µg/m³")

    # Visualisasi 1: Tren Bulanan
    st.subheader("Tren Bulanan Konsentrasi PM2.5")
    monthly_df = main_df.resample(rule='ME', on='datetime').agg({"PM2.5": "mean"}).reset_index()

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(monthly_df['datetime'], monthly_df['PM2.5'], marker='o', linewidth=2, color="#3498db")
    ax.set_ylabel("PM2.5 (µg/m³)", fontsize=15)
    st.pyplot(fig)

    # Visualisasi 2: Tren Per Jam
    st.subheader("Pola Polusi Berdasarkan Jam")
    hourly_df = main_df.groupby("hour").agg({"PM2.5": "mean"}).reset_index()

    fig, ax = plt.subplots(figsize=(16, 8))
    # Memberi warna berbeda untuk nilai tertinggi
    colors = ["#D3D3D3" if x < max(hourly_df['PM2.5']) else "#e74c3c" for x in hourly_df['PM2.5']]
    sns.barplot(x="hour", y="PM2.5", data=hourly_df, palette=colors, ax=ax)
    ax.set_ylabel("PM2.5 (µg/m³)", fontsize=15)
    ax.set_xlabel("Jam", fontsize=15)
    st.pyplot(fig)

    st.caption('Copyright (c) Submission Dicoding 2026')

except FileNotFoundError:
    st.error(
        "File CSV tidak ditemukan! Pastikan file 'PRSA_Data_Guanyuan_20130301-20170228.csv' berada di folder yang sama dengan script.")

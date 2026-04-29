import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Kualitas Udara Guanyuan", layout="wide")


# 1. Fungsi Load & Preprocessing Data
@st.cache_data  # Menggunakan cache agar loading lebih cepat
def load_data():
    # Pastikan file CSV berada di direktori yang sama
    df = pd.read_csv("PRSA_Data_Guanyuan_20130301-20170228.csv")

    # Mengonversi waktu menjadi datetime
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

    # Cleaning: Menangani missing values dengan interpolasi linear (seperti di notebook)
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = df[numeric_cols].interpolate(method='linear', limit_direction='forward', axis=0)

    return df


all_df = load_data()

# --- SIDEBAR (FITUR INTERAKTIF) ---
with st.sidebar:
    st.header("Konfigurasi Dashboard")

    # Filter 1: Rentang Waktu
    min_date = all_df["datetime"].min()
    max_date = all_df["datetime"].max()

    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Filter 2: Pilihan Parameter (Interaktivitas Tambahan)
    parameter = st.selectbox(
        label="Pilih Parameter Polutan",
        options=('PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'),
        index=0
    )

# Filter dataframe berdasarkan input user
main_df = all_df[(all_df["datetime"] >= pd.to_datetime(start_date)) &
                 (all_df["datetime"] <= pd.to_datetime(end_date))]

# --- MAIN PAGE ---
st.title("📊 Analisis Kualitas Udara Stasiun Guanyuan")
st.markdown(f"Dashboard ini menampilkan analisis data polusi udara berdasarkan filter yang dipilih.")

# Metrics Ringkasan
col1, col2, col3 = st.columns(3)
with col1:
    avg_val = round(main_df[parameter].mean(), 2)
    st.metric(f"Rata-rata {parameter}", value=avg_val)
with col2:
    max_val = main_df[parameter].max()
    st.metric(f"Konsentrasi Tertinggi", value=max_val)
with col3:
    min_val = main_df[parameter].min()
    st.metric(f"Konsentrasi Terendah", value=min_val)

st.divider()

# --- MENJAWAB PERTANYAAN 1: TREN BULANAN ---
st.subheader(f"1. Tren Konsentrasi {parameter} Rata-rata Bulanan")
monthly_df = main_df.resample(rule='ME', on='datetime').agg({
    parameter: "mean"
}).reset_index()

fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(monthly_df["datetime"], monthly_df[parameter], marker='o', linewidth=2, color="#2E86C1")
ax1.set_title(f"Perubahan Konsentrasi {parameter} per Bulan", fontsize=15)
ax1.set_xlabel("Tahun", fontsize=10)
ax1.set_ylabel(f"Konsentrasi (µg/m³)", fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig1)

with st.expander("Lihat Analisis Tren"):
    st.write(f""" 
    Terlihat bahwa konsentrasi {parameter} di Guanyuan bersifat fluktuatif. 
    Secara historis, lonjakan sering terjadi pada bulan-bulan dingin (Januari-Februari) 
    akibat peningkatan penggunaan bahan bakar pemanas atau faktor meteorologi.
    """)

# --- MENJAWAB PERTANYAAN 2: POLA HARIAN (JAM) ---
st.subheader(f"2. Pola Konsentrasi {parameter} Berdasarkan Jam dalam Sehari")
hourly_df = main_df.groupby("hour").agg({
    parameter: "mean"
}).reset_index()

# Cari jam puncak dan terendah untuk highlight
peak_hour = hourly_df.loc[hourly_df[parameter].idxmax(), 'hour']
low_hour = hourly_df.loc[hourly_df[parameter].idxmin(), 'hour']

fig2, ax2 = plt.subplots(figsize=(12, 5))
sns.barplot(
    x="hour",
    y=parameter,
    data=hourly_df,
    palette=["#D3D3D3" if x != peak_hour else "#E74C3C" for x in hourly_df.hour],
    ax=ax2
)
ax2.set_title(f"Rata-rata Konsentrasi {parameter} per Jam", fontsize=15)
ax2.set_xlabel("Jam (00:00 - 23:00)", fontsize=10)
ax2.set_ylabel(f"Konsentrasi (µg/m³)", fontsize=10)
st.pyplot(fig2)

# Kesimpulan Jawaban Pertanyaan 2
st.info(f"""
**Jawaban Pertanyaan Bisnis 2:**
- **Puncak Polusi:** Rata-rata konsentrasi {parameter} tertinggi terjadi pada pukul **{int(peak_hour)}:00**.
- **Kualitas Udara Terbaik:** Terjadi pada pukul **{int(low_hour)}:00**, di mana konsentrasi polutan berada pada titik terendah.
- Analisis ini membantu warga untuk membatasi aktivitas luar ruangan di jam-jam puncak tersebut.
""")

st.caption('Copyright (c) Submission Dicoding 2026')

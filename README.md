# Air Quality Dashboard - Guanyuan Station ✨

## Deskripsi
Dashboard ini merupakan proyek analisis data kualitas udara di stasiun Guanyuan. Aplikasi ini memungkinkan pengguna untuk memantau tren konsentrasi PM2.5 berdasarkan rentang waktu tertentu serta melihat pola polusi harian (per jam).

## Fitur
- **Metrik Utama**: Menampilkan rata-rata dan nilai maksimum PM2.5 pada periode terpilih.
- **Visualisasi Tren Bulanan**: Grafik garis yang menunjukkan fluktuasi PM2.5 dari waktu ke waktu.
- **Pola Polusi Per Jam**: Grafik batang yang menyoroti jam-jam dengan tingkat polusi tertinggi.
- **Filter Interaktif**: Sidebar untuk memfilter data berdasarkan tanggal.

## Struktur Proyek
- `dashboard.py`: File utama aplikasi Streamlit.
- `PRSA_Data_Guanyuan_20130301-20170228.csv`: Dataset kualitas udara.
- `requirements.txt`: Daftar pustaka yang diperlukan.
- `notebook.ipynb`: File analisis data awal.

## Setup Environment - Anaconda
```bash
conda create --name airquality-ds python=3.9
conda activate airquality-ds
pip install -r requirements.txt
